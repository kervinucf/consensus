import time
from cleantext import clean
import json
import re
from dataclasses import dataclass
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.entities.user import UserEntity
from server.gateways.data.resources.providers.geo.sources.Nominatim.helpers import find_coordinates


def extract_content(tweet):
    """
    format a tweet object from the data.
    """

    ################################################################################
    ################################ FIX ###########################################
    ################################################################################
    # find space types from included
    # find tweet types from included
    retweet = False
    ################################################################################
    ################################################################################
    ################################################################################

    try:
        geo = tweet['geo']
    except KeyError:
        geo = None

    _type = 'text'

    try:
        media_keys = tweet['attachments']['media_keys']
        _type = 'media'
    except KeyError:
        media_keys = None
    try:
        poll_ids = tweet['attachments']['poll_ids']
        _type = 'poll'
    except KeyError:
        poll_ids = None

    try:
        entities = tweet['entities']
    except KeyError:
        entities = None

    return {
        'id': tweet['id'],
        'owner_id': tweet['author_id'],
        'created_at': tweet['created_at'],
        'conversation_id': tweet['conversation_id'],
        'content': {
            'lang': tweet['lang'],
            'text': tweet['text'],
            'isRetweet': retweet,
        },
        'metrics': tweet['public_metrics'],
        "geo": geo,
        "media_keys": media_keys,
        "poll_ids": poll_ids,
        "entities": entities,
        'types': _type,
    }


def create_meta(owner, data):

    if data['geo']:
        location = data['geo']
        location_derived = 'geo'
    else:
        location = owner['coordinates']
        location_derived = 'profile'

    sentiment = None

    matching_rule = ''

    return {
        'geo': location,
        'location_derived': location_derived,
        'sentiment': '',
        'tag': matching_rule
    }


@dataclass
class TweetEntity:

    def __init__(self, res_data):
        # ################################################################################
        self.owner = None
        # ################################################################################
        # res[includes]
        # #############
        self.media = None
        self.polls = None
        self.places = None
        # ################################################################################
        # data[entities]
        # add annotations later
        # ##############
        self.hashtags = None
        self.cashtags = None
        self.mentions = None
        self.urls = None
        # ################################################################################
        self.referenced_tweets = {}
        self.participants = {}
        # ################################################################################
        self.meta = None
        self.tag = None
        # ################################################################################
        self.tweet = extract_content(res_data)

        self.search_entities()
        self.tracker = None
        # ################################################################################

    def add_tag(self, matching_rules):
        self.tag = matching_rules[0]

    def add_tracker(self, stream_rule):
        try:
            rule_list = re.findall("\((.+?)\)", stream_rule)[0].split(" OR ")
            tweet_text = self.tweet["content"]["text"]
            self.tracker = re.findall(
                r"(?=(" + '|'.join(rule_list) + r"))", tweet_text)[0]
            return True
        except IndexError:
            return False

    def search_entities(self):
        try:
            self.hashtags = [hashtag['tag']
                             for hashtag in self.tweet['entities']['hashtags']]
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            self.mentions = [mention['id']
                             for mention in self.tweet['entities']['mentions']]
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            self.cashtags = [cashtag['tag']
                             for cashtag in self.tweet['entities']['cashtags']]
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            self.urls = [url['url'] for url in self.tweet['entities']['urls']]
        except KeyError:
            pass
        except TypeError:
            pass

    def streamable(self):
        # hash of geo - sentiment - tweet types -
        return json.dumps()

    def add_media(self, media_included):
        if media_included and self.tweet['media_keys']:
            self.media = [media_dict['media_key']
                          for media_dict in media_included if media_dict['media_key'] in self.tweet['media_keys']]

    def add_polls(self, polls_included):
        if polls_included and self.tweet['poll_ids']:
            self.polls = [poll_dict['id']
                          for poll_dict in polls_included if poll_dict['id'] in self.tweet['poll_ids']]

    def add_places(self, places_included):
        if places_included:
            self.places = [places_included["country"]
                           for places_included in places_included]

    def read_tweet_chain(self, tweets_included):

        if tweets_included:
            for tweet_dict in tweets_included:
                self.referenced_tweets[tweet_dict['id']
                                       ] = TweetEntity(tweet_dict).tweet
            # assign order?

    def assign_roles(self, users_included):

        if users_included:
            for user_dict in users_included:
                user_found = UserEntity(res_data=user_dict)
                if user_found.id != self.tweet['owner_id']:
                    self.participants[user_dict['id']] = user_found.__dict__
                else:
                    self.owner = user_found.__dict__
                    self.owner['coordinates'] = find_coordinates(location=self.owner['location'])

        self.meta = create_meta(owner=self.owner, data=self.tweet)

    def minify(self):
        participants = {}

        for user_id, user in self.participants.items():
            participants[user_id] = {
                "id": user["id"],
                "img": user["img"],
            }
        return {
            "owner": {
                "id": self.owner["id"],
                "img": self.owner["img"],
            },
            "participants": participants,
            "tweet": {
                "id": self.tweet["id"],
                "created_at": self.tweet["created_at"],
                "types": self.tweet["types"],
                "metrics": self.tweet["metrics"],
            },
            "tagged": self.tracker,
            "coordinates": self.owner["coordinates"],

        }
    # create minified object for stream

    # owner -> id - img - geo
    # participants -> id - img - geo
    # tweet -> types - mention count - media link - tweet_id
