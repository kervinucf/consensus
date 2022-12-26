from server.gateways.data.resources.providers.twtr.controller import TwitterAggregator
from server.gateways.data.resources.providers.weather.sources.EarthQuakeBot.helpers import EarthQuake


class EarthQuakeBotProvider:

    def __init__(self):
        pass

    @staticmethod
    def get_latest_earthquakes():
        earthquake_bot_tweets = TwitterAggregator().find_tweets(username='EarthQuakeBot')
        recent_earthquakes = []
        for tweet in earthquake_bot_tweets:
            earthquake_event = EarthQuake(tweet)
            if earthquake_event.recent:
                recent_earthquakes.append(earthquake_event.data)

        return recent_earthquakes
