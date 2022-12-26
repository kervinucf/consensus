from server.gateways.data.resources.providers.geo.sources.Nominatim.helpers import find_coordinates
from dataclasses import dataclass
import bisect
import flag
import pycountry


def get_country_flag_emoji(country_name):
    try:
        country_abb = pycountry.countries.get(name=country_name).alpha_2
        return flag.flag(country_abb)
    except AttributeError:
        return None


def add_in_order(_list, value):
    return bisect.insort(_list, value)


@dataclass
class PlaceEntity:
    def __init__(self, res_data):
        self.location = res_data["locations"][0]["name"]
        self.woeID = res_data["locations"][0]["woeid"]
        self.flag = get_country_flag_emoji(self.location)
        self.as_of = res_data["as_of"]
        self.created_at = res_data["created_at"]
        self.tweet_volume = 0
        self.coordinates = find_coordinates(location=self.location)

        trend_data_list = res_data["trends"]

        self.trends = {}

        for trend_data in trend_data_list:
            trend_entity = TrendEntity(res_data=trend_data)
            if 'and' not in trend_entity.name and '&' not in trend_entity.name:
                self.trends[trend_entity.name] = trend_entity.__dict__

        self.trending = sorted(self.trends.values(),
                               key=lambda d: d['tweet_volume'], reverse=True)

        for trend in self.trends.values():
            self.tweet_volume += trend['tweet_volume']

        self.top_ten = self.trending[:10]


@dataclass
class TrendEntity:

    def __init__(self, res_data):

        self.name = res_data['name']
        self.url = res_data['url']
        self.promoted_content = res_data['promoted_content']
        self.query = res_data['query']
        if res_data['tweet_volume']:
            self.tweet_volume = res_data['tweet_volume']
        else:
            self.tweet_volume = 0
