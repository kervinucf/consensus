from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.geo.controller import GeoAggregator


def validate_distance_request(request):
    distance_request_validator = RequestValidator()
    origin = None
    destination = None

    try:
        origin = request.get_json()['origin']
        destination = request.get_json()['destination']
        distance_request_validator.target_source = request.get_json()['source']

    except KeyError:
        pass

    if origin is None or destination is None:
        distance_request_validator.message = "Bad request"
        distance_request_validator.error = "Missing origin or destination parameter"
        return distance_request_validator.bad_request()

    # source is optional
    valid_sources = ['geo']

    if distance_request_validator.target_source is not None and distance_request_validator.target_source not in valid_sources:
        distance_request_validator.message = "Bad request"
        distance_request_validator.error = "Invalid source parameter"
        return distance_request_validator.bad_request()

    distance_request_validator.params = {
        'origin': origin, 'destination': destination}

    return distance_request_validator.valid_request()


def distance_cache_key(validated_request):
    return None


def distance_db_key(validated_request):
    return None


def distance_aggregator_endpoint(validated_request):

    validated_request.data = GeoAggregator(provider=validated_request.target_source)\
        .get_distance(validated_request.params['origin'], validated_request.params['destination'])
    if validated_request.data is None:
        validated_request.message = "Error retrieving distance"
        validated_request.error = "Failed to retrieve distance"
        return validated_request.internal_server_error()

    return validated_request
