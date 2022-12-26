from server.gateways.data.resources.providers.weather.sources.EarthQuakeBot.utils import EarthQuake


def get_latest_earthquakes():
    # earthquakeBot - 122264472
    # check db
    recent_earthquakes = []
    # #####################################################################
    #api_earthquakes = MyGateway(endpoint="/find_user_tweets", params={"user_id": "122264472"})
    api_earthquakes = None
    # #####################################################################
    if api_earthquakes:
        for tweet in api_earthquakes.json()['data']:
            earthquake_event = EarthQuake(tweet)
            if earthquake_event.recent:
                recent_earthquakes.append(earthquake_event.data)

        if len(recent_earthquakes) > 0:
            return recent_earthquakes
        else:
            return None
