from lib.Twitter.api.entities.tweet import TweetEntity
from lib.API.Gateway import MyGateway
from npc_network_news.backend.lib.Redis.resources import publish, get_redis
from lib.Mongo.resources.utils import update_record, get_from_db, delete_record, get_table
import time

from lib.API.helpers.stream_rules import RuleManager
import json
from lib.Twitter.api.endpoints.utils.helpers import get_current_time, time_passed, convert_to_seconds
from server.lib.utils.logger import status_logger


def publish_to_stream(content, stream="conversation-live"):
    # stuff
    publish(redis=get_redis(), channel=stream, content=content)


class StreamController:

    def __init__(self, database):
        # ###############################
        self.rule_manager = RuleManager()
        self.process = None
        self.db = database
        # ###############################
        self.rules_set = False
        self.running = False
        self.up_to_date = False
        self.dynamic_topics = {}
        # ###############################
        self.sampling = 1
        self.tweet_count = 0
        self.tweet_limit_per_minute = None
        self.time_to_reset = None
        self.event_expiration = {}
        self.rules = {}

    def sampling_changed(self, sample):

        def calc_tweet_limit():

            return 40

        if self.tweet_limit_per_minute is None:
            # set up tweet limit
            self.tweet_limit_per_minute = calc_tweet_limit()

        if self.time_to_reset is None:
            self.time_to_reset = get_current_time(
                future=convert_to_seconds(minutes=1))

        self.tweet_count += 1

        status_logger(
            non_status_text='\033[94m' + '\n **** {} conversation found ****'.format(self.tweet_count) + '\033[00m')
        status_logger(non_status_text="time passed {} \n".format(
            self.time_to_reset - get_current_time()))

        if self.tweet_count > self.tweet_limit_per_minute:
            status_logger(status_text="Tweet limit reached", red=True)
            self.tweet_count = 0
            self.sampling -= 1
            return True

        if time_passed(last_update=get_current_time(), expiration_time=self.time_to_reset):
            status_logger(status_text="Time limit reached - count: {} limit: {}".format(self.tweet_count,
                                                                                        self.tweet_limit_per_minute),
                          red=True)
            time.sleep(5)
            if self.tweet_count < self.tweet_limit_per_minute:
                self.sampling += 1
                self.tweet_count = 0
                return True

            self.tweet_count = 0
            self.time_to_reset = get_current_time(
                future=convert_to_seconds(minutes=1))

    def message_handler(self, stream_message):

        def deconstruct_stream_message(response):
            res = json.loads(response)

            # ####################################################
            # ####################################################
            # Tweet
            # create tweet entity
            # save tweet
            tweet_object = TweetEntity(res_data=res['data'])
            try:
                stream_rules = res['matching_rules']
                tweet_object.add_tag(matching_rules=stream_rules)
            except KeyError:
                pass
            # ####################################################
            # ####################################################
            try:
                stream_includes = res['includes']
                try:
                    # ####################################################
                    # ####################################################
                    # Referenced Tweets
                    # create tweet entity
                    # save tweet
                    tweets = stream_includes['conversation']
                    tweet_object.read_tweet_chain(tweets_included=tweets)
                    # ####################################################
                    # ####################################################
                except KeyError:
                    pass

                try:
                    # ####################################################
                    # ####################################################
                    # Participants
                    # create tweet entity
                    # save tweet
                    users = stream_includes['users']
                    tweet_object.assign_roles(users_included=users)
                    # ####################################################
                    # ####################################################
                except KeyError:
                    pass

                try:
                    # ####################################################
                    # ####################################################
                    # Media
                    # create tweet entity
                    # save tweet
                    users = stream_includes['media']
                    tweet_object.add_media(media_included=users)
                    # ####################################################
                    # ####################################################
                except KeyError:
                    pass

                try:
                    # ####################################################
                    # ####################################################
                    # Polls
                    # create tweet entity
                    # save tweet
                    users = stream_includes['polls']
                    tweet_object.add_polls(polls_included=users)

                    # ####################################################
                    # ####################################################
                except KeyError:
                    pass

            except KeyError:
                pass

            return tweet_object

        def save_tweet(obj):

            # save owner
            # save participants
            # save tweet
            update_record(db=self.db, table='conversation',
                          column=obj.tweet['id'], data=obj.tweet)
            update_record(db=self.db, table='users',
                          column=obj.owner['id'], data=obj.owner)

            for participant in obj.participants.items():
                update_record(db=self.db, table='users',
                              column=participant[1]['id'], data=participant[0])

            for referenced_tweet in obj.referenced_tweets.items():
                update_record(db=self.db,
                              table='conversation',
                              column=referenced_tweet[1]['id'],
                              data=referenced_tweet[0])
            # ####################################################
            # ####################################################
            update_record(db=self.db, table='Playback',
                          column=obj.tweet['id'], data=obj.__dict__)

        def publish_to_redis_channels(msg, rules):
            # time.sleep(4)
            new_tweet = json.dumps(msg.__dict__)
            if not msg.tracker:
                try:
                    rule_list = rules[msg.tag['id']]['value']
                    if msg.add_tracker(rule_list):
                        publish_to_stream(content=new_tweet,
                                          stream=msg.tracker)
                except AttributeError:
                    pass

            publish_to_stream(content=new_tweet, stream=msg.tag['tag'])
            publish_to_stream(content=new_tweet, stream='twitter_filtered')

        tweet_entity = deconstruct_stream_message(response=stream_message)

        save_tweet(obj=tweet_entity)
        publish_to_redis_channels(msg=tweet_entity, rules=self.rules)

        if self.sampling_changed(sample=tweet_entity.tag['tag']):
            status_logger(status_text="Updating sampling rate", red=True)
            update_record(db=self.db, table='StreamingRules',
                          column="ResetState", data=True)

        status_logger(non_status_text='\033[93m' + 'PROCESSED TWEET --> {}'.format(
            tweet_entity.minify()) + '\033[00m')

    def stream_requires_reset(self):
        return get_from_db(db=self.db, table='StreamingRules', column='ResetState')

    def find_active_rules(self):
        def check_db_for(rule_set):

            rule_ids_saved_in_db = get_from_db(
                db=self.db,
                table='StreamingRules',
                column='Current'
            )
            if not rule_ids_saved_in_db:
                rule_ids_saved_in_db = []
            else:
                rule_ids_saved_in_db = rule_ids_saved_in_db

            return set(rule_set) - set(rule_ids_saved_in_db)

        result = MyGateway(endpoint='/get_rules')
        if result:
            rules_dynamic_on_twitter = result.json()
        else:
            rules_dynamic_on_twitter = None
        status_logger(non_status_text="Rules on Twitter: {}".format(
            rules_dynamic_on_twitter))

        if rules_dynamic_on_twitter and rules_dynamic_on_twitter['data']:
            self.rules = rules_dynamic_on_twitter['data']['rules_found']

            rule_ids_not_in_db = check_db_for(
                rule_set=rules_dynamic_on_twitter['data'])

            if not rule_ids_not_in_db:
                status_logger(status_text=(
                    'Twitter gateways rules match saved rules'), green=True)
            else:
                status_logger(
                    status_text='Twitter gateways rules do not match saved rules -> {}'.format(rule_ids_not_in_db), red=True)
                status_logger(status_text='Saving new rules', yellow=True)
                # rules to save -> list of RuleDict {'id': ex., 'value': ex., 'tag': ex.}
                # add individual new rules to db by id
                for rule_id in rule_ids_not_in_db:
                    update_record(
                        db=self.db,
                        table='StreamingRules',
                        column=rule_id,
                        data=rules_dynamic_on_twitter['data'][rule_id]
                    )
                # add current rules to db
                update_record(
                    db=self.db,
                    table='StreamingRules',
                    column='Current',
                    data=rules_dynamic_on_twitter['data']
                )
            self.rules_set = True
        else:
            status_logger(
                status_text='Twitter gateways rules not present', red=True)
            self.__setup_dynamic_rules()

    def add_rule(self,
                 adding_rule_set,
                 ttl,
                 event,
                 _type
                 ):

        if adding_rule_set:
            rules_added = MyGateway(
                endpoint='/add_rules',
                params={
                    'rule_set': {"rules": list(adding_rule_set)},
                    'event': event,
                    'ttl': ttl,
                    'types': _type,
                    'sample': self.sampling
                }
            )

            if rules_added and rules_added.json()['data']:
                status_logger(
                    non_status_text='\033[92m' + 'Added rules: {}'.format(adding_rule_set) + '\033[0m')

                self.event_expiration[event] = get_current_time(future=ttl)

    def remove_rule(self, removing_rule_set, event):
        # removing rules on conversation
        rules_removed = MyGateway(
            endpoint='/delete_rules',
            params={
                'rule_set': {"rules": list(removing_rule_set)},
                'event': event,
            }
        )

        if rules_removed and rules_removed.json()['data']:
            status_logger(
                non_status_text='\033[92m' + 'Removed rules: {}'.format(removing_rule_set) + '\033[0m')
            return True

    def __setup_dynamic_rules(self):

        # #################################
        # base rules to track (25 rules)
        # Misc [ 5 ]
        # from gateways -- wordle, severe events, verzuz, random thread etc... elections?
        # #################################
        # Finance  [ 3 ]
        FINANCE_RULES_TO_ADD = self.rule_manager.CreateFinanceRules()
        # crypto
        # stocks
        # currency
        if FINANCE_RULES_TO_ADD:
            finance_rules = FINANCE_RULES_TO_ADD.keys()
            status_logger(
                status_text=f"Adding Finance Rules -> {finance_rules}", pink=True)
            try:
                finance_topics = self.dynamic_topics['Finance']
            except KeyError:
                finance_topics = []

            for finance_rule in finance_rules:
                finance_topics.append(finance_rule)
                self.dynamic_topics['Finance'] = finance_topics
                self.add_rule(adding_rule_set=FINANCE_RULES_TO_ADD[finance_rule],
                              ttl=convert_to_seconds(minutes=15),
                              _type="CASHTAG",
                              event=finance_rule)

        # Providers [ 6 ]
        SOURCES_RULES_TO_ADD = self.rule_manager.CreateEventRules()
        if SOURCES_RULES_TO_ADD:
            source_rules = SOURCES_RULES_TO_ADD.keys()
            status_logger(
                status_text=f"Adding Source Rules -> {source_rules}", pink=True)
            for source_rule in source_rules:
                self.add_rule(adding_rule_set=SOURCES_RULES_TO_ADD[source_rule],
                              ttl=convert_to_seconds(days=7),
                              _type="FROM_USER",
                              event=source_rule)
        # Trending [ 5 ]
        TRENDING_RULES_TO_ADD = self.rule_manager.CreateTrendingRules()
        if TRENDING_RULES_TO_ADD:
            status_logger(status_text="Adding Trending Rules", pink=True)
            # by continent - na, sa, eu, as, af
            trending_rules = TRENDING_RULES_TO_ADD.keys()
            try:
                trending_topics = self.dynamic_topics['Trending']
            except KeyError:
                trending_topics = []
            for trending_rule in trending_rules:
                trending_topics.append(trending_rule)
                self.dynamic_topics['Trending'] = trending_topics
                self.add_rule(adding_rule_set=TRENDING_RULES_TO_ADD[trending_rule],
                              ttl=convert_to_seconds(minutes=15),
                              _type="HASHTAG",
                              event=trending_rule)
        # Games [ 5 ]
        SPORTS_RULES_TO_ADD = self.rule_manager.CreateSportsRules()
        if SPORTS_RULES_TO_ADD:
            sports_rules = SPORTS_RULES_TO_ADD.keys()
            status_logger(status_text='Adding sports rules {}'.format(
                sports_rules), pink=True)
            # by league - nfl, mlb, nba, soccer, f1
            try:
                sports_topics = self.dynamic_topics['Sports']
            except KeyError:
                sports_topics = []
            for sports_rule in sports_rules:
                sports_topics.append(sports_rule)
                self.dynamic_topics['Sports'] = sports_topics
                self.add_rule(adding_rule_set=SPORTS_RULES_TO_ADD[sports_rule],
                              ttl=convert_to_seconds(hours=6),
                              _type="KEYWORD",
                              event=sports_rule)

        self.rules_set = True

    def __get_topics(self):
        try:
            events_expiring = get_table(
                db=self.db, table_name='ExpiredAt')
            for x in events_expiring.find():
                self.event_expiration[x['field']] = x['entry']
            status_logger(
                status_text="STREAMING TOPICS --> {}".format(self.event_expiration.keys()), cyan=True)
            return self.event_expiration.keys()
        except Exception as e:
            status_logger(non_status_text=e)

    def __removing_expired_topics(self, events_to_watch):
        conversation_updated = False
        ongoing_conversations = self.dynamic_topics.values()
        for event in events_to_watch:

            if get_current_time() > self.event_expiration[event]:
                status_logger(status_text='{} EXPIRED'.format(event), red=True)
                rules_to_remove = get_from_db(
                    db=self.db, table='StreamingRules', column=event)
                if self.remove_rule(removing_rule_set=rules_to_remove, event=event):
                    status_logger(status_text='Removed rules: {}'.format(
                        rules_to_remove), red=True)
                    if event in ongoing_conversations:
                        self.__update_dynamic_topics(event)
                    conversation_updated = True
            else:
                continue
        return conversation_updated

    def __update_dynamic_topics(self, event):

        rules_to_add = None
        if event in self.dynamic_topics['Finance']:
            rules_to_add = self.rule_manager.CreateFinanceRules()
            expiration = convert_to_seconds(minutes=15)
            _type = "CASHTAG"

        elif event in self.dynamic_topics['Trending']:
            rules_to_add = self.rule_manager.CreateTrendingRules()
            expiration = convert_to_seconds(minutes=15)
            _type = "HASHTAG"

        elif event in self.dynamic_topics['Sports']:
            rules_to_add = self.rule_manager.CreateSportsRules()
            expiration = convert_to_seconds(hours=6)
            _type = "KEYWORD"

        if rules_to_add:
            rules_to_add = rules_to_add.keys()
            for rule in rules_to_add:
                self.add_rule(adding_rule_set=rule,
                              ttl=expiration,
                              event=event,
                              _type=_type)

    def monitor_global_conversation(self):
        status_logger(status_text="Monitoring Global Conversation", pink=True)
        # #################################################################
        # check events to see if they've expired
        # #################################################################
        events_to_watch = self.__get_topics()
        if events_to_watch:
            if self.__removing_expired_topics(events_to_watch) or self.stream_requires_reset():
                status_logger(
                    status_text="MONITORING REQUIRES RESET", red=True)
                self.up_to_date = False
        else:
            status_logger(status_text="NO ACTIVE TOPICS TO FOLLOW", red=True)
