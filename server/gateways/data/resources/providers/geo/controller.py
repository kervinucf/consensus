from server.gateways.data.resources.providers.geo.sources.Nominatim.interface import NominatimProvider
from server.gateways.data.resources.providers.geo.sources.Nominatim.helpers import find_coordinates, get_distance, get_countries_from_db, get_cities_from_db, get_country, get_city
import datetime
import pytz


class GeoAggregator:

    def __init__(self, provider=None):
        pass

    @staticmethod
    def get_location_time(timezone):
        tz = pytz.timezone(timezone)
        if tz:
            return datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    def get_city(self, city):
        city = get_city(city)
        if city:
            try:
                city_timezone = city['timezone']
                if city_timezone:
                    city['time'] = self.get_location_time(city_timezone)
            except KeyError:
                pass

        return city

    @staticmethod
    def get_cities():
        return get_cities_from_db()

    @staticmethod
    def get_country(country):
        return get_country(country)

    @staticmethod
    def get_countries():
        return get_countries_from_db()

    @staticmethod
    def locate_coordinates(location=None, city=False):
        # location = {
        #    'country': 'United States',
        #    'city': 'New York'
        # }

        if city:
            coordinates = find_coordinates(city=location['city'], country=location['country'])
        else:
            coordinates = find_coordinates(location=location)
        return coordinates

    def calculate_distance(self, locations):
        location1 = self.locate_coordinates(locations['location1'])
        location2 = self.locate_coordinates(locations['location2'])

        if location1 and location2:
            loc1 = tuple(location1.values())
            loc2 = tuple(location2.values())
            return get_distance(loc1, loc2)


