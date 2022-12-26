from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.geo.controller import GeoAggregator


def validate_country_request(request):
    country_request_validator = RequestValidator()
    country = None
    find_all = False

    try:
        country = request.get_json()['country']
    except KeyError:
        find_all = request.get_json()['find_all']

    try:
        country_request_validator.target_source = request.get_json()['source']
    except KeyError:
        pass

    if country is None and not find_all:
        country_request_validator.message = "Bad request"
        country_request_validator.error = "Missing country parameter"
        return country_request_validator.bad_request()

    if country and find_all:
        country_request_validator.message = "Bad request"
        country_request_validator.error = "Cannot specify both country and find_all"
        return country_request_validator.bad_request()

    # source is optional
    valid_sources = ['geo']
    if country_request_validator.target_source is not None and country_request_validator.target_source not in valid_sources:
        country_request_validator.message = "Bad request"
        country_request_validator.error = "Invalid source parameter"
        return country_request_validator.bad_request()

    if find_all:
        country_request_validator.params = {'find_all': find_all}
    else:
        country_request_validator.params = {'country': country}

    return country_request_validator.valid_request()


def country_cache_key(validated_request):
    return None


def country_db_key(validated_request):
    return None


def country_aggregator_endpoint(validated_request):
    try:
        validated_request.data = GeoAggregator(provider=validated_request.target_source) \
            .get_country(country=validated_request.params['country'])
    except KeyError:
        validated_request.data = GeoAggregator(provider=validated_request.target_source) \
            .get_countries()
    if validated_request.data is None:
        validated_request.message = "Error retrieving country data"
        validated_request.error = "Failed to retrieve country data"
        return validated_request.internal_server_error()

    return validated_request
