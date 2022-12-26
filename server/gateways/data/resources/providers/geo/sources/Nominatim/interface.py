from server.gateways.data.resources.providers.geo.sources.Nominatim.helpers import get_countries_from_db,\
    get_cities_from_db, get_timezones, available_timezones


class NominatimProvider:

    def __init__(self):
        pass

    @staticmethod
    def search_available_countries():
        # find all available countries
        # this will  return a list of countries
        # from the database although initially from helpers file
        return get_countries_from_db()

    def search_country_by_name(self, country):
        return self.search_available_countries()[country]

    @staticmethod
    def search_available_cities():
        return get_cities_from_db()

    def search_city_by_name(self, city):
        return self.search_available_cities()[city]

    # get timezones
    @staticmethod
    def search_available_timezones():
        # find all available timezones
        return available_timezones()

    def search_timezone_by_name(self, timezone):
        return self.search_available_timezones()[timezone]


