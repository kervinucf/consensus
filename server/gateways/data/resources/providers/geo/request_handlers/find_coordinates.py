from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.geo.controller import GeoAggregator


def validate_coordinates_request(request):
    coordinates_request_validator = RequestValidator()

    try:
        city = request.get_json()["city"]
        country = request.get_json()["country"]
    except KeyError:
        city = None
        country = None

    try:
        location = request.get_json()['location']
    except KeyError:
        location = None

    if location is None and country is None and city is None:
        coordinates_request_validator.message = "Bad request"
        coordinates_request_validator.error = "Missing location, city, or country parameter"
        return coordinates_request_validator.bad_request()

    if location is not None and (city is not None or country is not None):
        coordinates_request_validator.message = "Bad request"
        coordinates_request_validator.error = "Location parameter cannot be used with city or country parameters"
        return coordinates_request_validator.bad_request()

    # source is optional
    valid_sources = ['geo']
    if coordinates_request_validator.target_source is not None and coordinates_request_validator.target_source not in valid_sources:
        coordinates_request_validator.message = "Bad request"
        coordinates_request_validator.error = "Invalid source parameter"
        return coordinates_request_validator.bad_request()

    if location is not None:
        coordinates_request_validator.params = {"location": location}

    if city is not None and country is not None:
        coordinates_request_validator.params = {"location": {
            "city": city, "country": country
        }}

    return coordinates_request_validator.valid_request()


def coordinates_cache_key(validated_request):
    return None


def coordinates_db_key(validated_request):
    return None


def coordinates_aggregator_endpoint(validated_request):
    try:
        city = validated_request.params['location']['city']
        validated_request.data = GeoAggregator(
            provider=validated_request.target_source).locate_coordinates(location=validated_request.params['location'],
                                                                         city=True)
    except TypeError:
        validated_request.data = GeoAggregator(
            provider=validated_request.target_source).locate_coordinates(location=validated_request.params['location'])

    if validated_request.data is None:
        validated_request.message = "Error retrieving coordinates"
        validated_request.error = "Failed to retrieve coordinates"
        return validated_request.internal_server_error()

    return validated_request
