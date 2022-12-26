from server.gateways.data.resources.providers.twtr.sources.Twitter.interfaces.trends import TrendsProvider
from server.gateways.data.resources.providers.twtr.sources.Twitter.interfaces.users import UserProvider
from server.gateways.data.resources.providers.twtr.sources.Twitter.interfaces.tweets import TweetsProvider
from server.gateways.data.resources.providers.twtr.sources.Twitter.interfaces.spaces import SpacesProvider


class TwitterAggregator:

    tweets = TweetsProvider()
    users = UserProvider()
    trends = TrendsProvider()
    spaces = SpacesProvider()

    def __init__(self):
        pass

    def find_tweets(self, _id=None, _id_list=None, search_term=None,  username=None, max_results=10):
        if _id:
            conversation = self.tweets.lookup_conversation(conversation_id=_id, max_results=max_results)
            return conversation

        elif _id_list:
            tweets = self.tweets.lookup_tweets(tweet_id_list=_id_list)
            return tweets

        elif search_term:
            tweets = self.tweets.search_for_tweets(search_term=search_term, max_results=max_results)
            return tweets

        else:
            #
            user_id = self.find_user(user_name=username)['id']
            tweets = self.tweets.lookup_user_tweets(user_id=user_id, max_results=max_results)
            return tweets

    def find_spaces(self, _id=None, search_term=None, top=None):
        if _id:
            spaces = self.spaces.lookup_space(space_id=_id)
            return spaces

        elif search_term:
            spaces = self.spaces.search_for_spaces(search_term=search_term)
            return spaces

        elif top:
            top_spaces = self.spaces.lookup_top_spaces()
            return top_spaces

    def find_user(self, user_name):
        user = self.users.lookup_user(user_name=user_name)
        return user

    def find_trends(self, location=None, _global=None):

        if location:
            location_trends = self.trends.search_trends_in(location=location)
            return location_trends

        if _global:
            global_trends = self.trends.global_trends()
            return global_trends

    def stream_rules(self, get=None, add=None, delete=None, active=None, streaming=None):

        if get:
            return self.lookup_rules()
        elif add:
            return self.add_rules(add)
        elif delete:
            return self.delete_rules(delete)

        elif streaming:
            def lookup_active_streams(db_key):
                if db_key.exists():
                    return db_key.value

            return lookup_active_streams(active)
