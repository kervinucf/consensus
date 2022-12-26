from server.gateways.data.resources.providers.twtr.sources.Twitter.api.resolver import TwitterQuery


class TweetsProvider:

    @staticmethod
    def lookup_conversation(conversation_id, max_results=10):
        api_conversation = TwitterQuery(
            conversation_id=conversation_id, max_results=max_results)
        if api_conversation:
            return [tweet.__dict__ for tweet in api_conversation]
        else:
            return None

    @staticmethod
    def search_for_tweets(search_term, max_results=10):
        if search_term:
            api_tweets = TwitterQuery(
                tweet_search=search_term, max_results=max_results)
            if api_tweets:
                return [tweet.__dict__ for tweet in api_tweets]
            else:
                return None

    @staticmethod
    def lookup_tweets(tweet_id_list):

        if type(tweet_id_list) == str:
            tweet_id_list = [tweet_id_list]
        api_tweet = TwitterQuery(tweet_id_list=tweet_id_list)
        if api_tweet:
            return [tweet.__dict__ for tweet in api_tweet]
        else:
            return None

    @staticmethod
    def lookup_user_tweets(user_id, max_results=10):

        if user_id:
            api_tweets = TwitterQuery(user_tweets=user_id, max_results=max_results)
            if api_tweets:
                return [tweet.__dict__ for tweet in api_tweets]
            else:
                return None
