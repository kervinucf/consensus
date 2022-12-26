from geopy import distance
import pytz
import datetime
import geonamescache
from dataclasses import dataclass
from server.lib.utils.database import get_transaction, get_from_db, update_record, get_db
from server.gateways.data.resources.providers.geo.sources.Nominatim.utils import get_coordinates, logger, \
    get_country_list, get_city_list, get_timezone


def get_distance(center_point, test_point):
    return distance.distance(center_point, test_point).km


def get_country(location):
    country = get_from_db(
        db=get_db('LocationDatabase'),
        table='Countries',
        column=location)

    if not country:
        logger.debug('{} country not found in db'.format(location))
        for country_name in get_country_list():
            if country_name == location:
                country = Country(country_name).__dict__
                update_record(db=get_db('LocationDatabase'), table='Countries',
                              column=location, data=country, forceNew=True)
                return country

    return country


def get_city(city):

    city_data = get_from_db(
        db=get_db('LocationDatabase'),
        table='Cities',
        column=city
    )
    if not city_data:
        logger.debug('{} city not found in db'.format(city))
        city_list = get_city_list()
        if city_list:
            for city_name in city_list:
                if city_name == city:
                    city_data = City(city_name).__dict__
                    update_record(db=get_db('LocationDatabase'), table='Cities',
                                  column=city, data=city, forceNew=True)
                    return city_data

    return city_data


def get_countries_from_db():
    CountriesCollection = get_db('LocationDatabase')['Countries']
    return get_transaction(CountriesCollection)


def get_cities_from_db():
    CitiesCollection = get_db('LocationDatabase')['Cities']
    return get_transaction(CitiesCollection)


def find_coordinates(city=None, country=None, location=None):

    if city:

        country_information = get_country(country)
        abbreviation = country_information['abbreviation']

        city_data = get_city(city)
        try:
            city_country = city_data['country_code']
        except TypeError:
            city_country = None

        if city_country == abbreviation:
            return city_data['coordinates']
        else:
            location = f"{city}, {abbreviation}"
            # check with city-country
            coordinates = find_coordinates(location=location)
            CityObject = City().from_address(city=city, country=country, coordinates=coordinates)

            update_record(
                db=get_db('LocationDatabase'),
                table='Cities',
                column=f"{city}-{abbreviation}",
                data=vars(CityObject),
            )

            return coordinates

    if location:
        location = location.upper()
        coordinates = get_from_db(
            db=get_db('LocationDatabase'),
            table='Coordinates',
            column=location)

        if not coordinates:
            logger.debug('{} coordinates not found in db'.format(location))
            coordinates = get_coordinates(location)
            if coordinates:
                logger.debug('updating coordinates for {}'.format(location))

                update_record(db=get_db('LocationDatabase'), table='Coordinates',
                              column=location, data=coordinates, forceNew=True)
            else:
                logger.debug('coordinates not found for {}'.format(location))
                return None

        else:
            logger.debug(
                '{} coordinates found in db -> {}'.format(location, coordinates))

        return coordinates


def find_locations_available():
    available_locations = {}
    for available_location in get_db('LocationDatabase')["Coordinates"].find():
        available_locations[available_location["column"]
        ] = available_location["row"]
    return available_locations

@dataclass
class City:
    geonameid = None
    name = None
    coordinates = None
    continent = None
    country_code = None
    population = None
    timezone = None

    def __init__(self, city_name=None):
        if city_name:
            city_info = get_city(city_name)
            self.fill_city(city_info)

    def fill_city(self, city_info):
        city_data = list(city_info[0].values())[0]
        self.geonameid = city_data["geonameid"]
        self.name = city_data["name"]
        self.coordinates = {
            "lat": city_data["latitude"],
            "lng": city_data["longitude"]
        }
        self.continent = city_data["countrycode"]
        self.country_code = city_data["countrycode"]
        self.population = city_data["population"]
        self.timezone = city_data["timezone"]

    def from_address(self, city, country, coordinates):
        self.geonameid = None
        self.name = city
        self.country_code = country
        self.coordinates = coordinates
        self.continent = None
        self.population = None
        self.timezone = get_timezone(
            coordinates["lat"], coordinates["lng"]
        )
        return self


@dataclass
class Country:
    exists = False

    def __init__(self, country_name):
        country_data = geonamescache.GeonamesCache().get_countries_by_names()[
            country_name]
        if country_data:
            self.name = country_name
            self.exists = True
            self.coordinates = find_coordinates(location=country_name)
            self.geonameid = country_data["geonameid"]
            self.abbreviation = country_data["iso"]
            self.continent = country_data["continentcode"]
            self.area = country_data["areakm2"]
            self.population = country_data["population"]
            self.currency_symbol = country_data["currencycode"]
            self.currency_name = country_data["currencyname"]
            self.phone = country_data["phone"]
            self.languages = country_data["languages"]
            self.neighbors = country_data["neighbours"]


def populate_country_db_collection():
    collection_db = get_db('LocationDatabase')['Countries']
    for country_name in get_country_list():
        country_data = Country(country_name).__dict__
        collection_db.update_one(
            {'column': country_name},
            {'$set': {'row': country_data}},
            upsert=True
        )

    return collection_db


def populate_city_db_collection():
    collection_db = get_db('LocationDatabase')['Cities']
    for city_name in get_city_list():
        city_data = City(city_name).__dict__
        if len(city_data) > 0:
            collection_db.update_one(
                {'column': city_name},
                {'$set': {'row': city_data}},
                upsert=True
            )
    return collection_db


# populate_city_db_collection()
# populate_country_db_collection()

def available_timezones():
    timezones = {}
    for cities in get_cities_from_db().items():
        try:
            city_timezone = timezones[cities[1]['timezone']]
            city_timezone.append(cities[0])
        except KeyError:
            timezones[cities[1]['timezone']] = [cities[0]]

    return timezones


def get_timezones(timezone):
    return available_timezones()[timezone]
