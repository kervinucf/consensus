from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.geo.controller import GeoAggregator


def validate_city_request(request):
    city_request_validator = RequestValidator()
    city = None
    find_all = False
    try:
        city = request.get_json()['city']
    except KeyError:
        find_all = request.get_json()['find_all']

    try:
        city_request_validator.target_source = request.get_json()['source']
    except KeyError:
        pass

    if city is None and not find_all:
        city_request_validator.message = "Bad request"
        city_request_validator.error = "Missing city parameter"
        return city_request_validator.bad_request()

    if city and find_all:
        city_request_validator.message = "Bad request"
        city_request_validator.error = "Cannot specify both city and find_all"
        return city_request_validator.bad_request()

        # source is optional
    valid_sources = ['geo']
    if city_request_validator.target_source is not None and city_request_validator.target_source not in valid_sources:
        city_request_validator.message = "Bad request"
        city_request_validator.error = "Invalid source parameter"
        return city_request_validator.bad_request()

    if find_all:
        city_request_validator.params = {'find_all': find_all}
    else:
        city_request_validator.params = {'city': city}

    return city_request_validator.valid_request()


def city_cache_key(validated_request):
    return


def city_db_key(validated_request):
    return None


def city_aggregator_endpoint(validated_request):
    try:
        validated_request.data = GeoAggregator(provider=validated_request.target_source) \
            .get_city(city=validated_request.params['city'])
    except KeyError:
        validated_request.data = GeoAggregator(provider=validated_request.target_source) \
            .get_cities()
    if validated_request.data is None:
        validated_request.message = "Error retrieving city data"
        validated_request.error = "Failed to retrieve city data"
        return validated_request.internal_server_error()

    return validated_request
