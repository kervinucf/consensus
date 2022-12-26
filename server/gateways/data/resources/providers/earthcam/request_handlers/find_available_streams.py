from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.earthcam.controller import EarthCamAggregator


def validate_stream_request(request):
    stream_request_validator = RequestValidator()
    location = None
    find_all = False

    try:
        location = request.get_json()['location']
    except KeyError:
        find_all = request.get_json()['find_all']

    try:
        stream_request_validator.target_source = request.get_json()['source']
    except KeyError:
        pass

    if location is None and not find_all:
        stream_request_validator.message = "Bad request"
        stream_request_validator.error = "Missing location parameter"
        return stream_request_validator.bad_request()

    if location and find_all:
        stream_request_validator.message = "Bad request"
        stream_request_validator.error = "Cannot specify both location and find_all"
        return stream_request_validator.bad_request()

    # source is optional
    valid_sources = ['youtube']
    if stream_request_validator.target_source is not None and stream_request_validator.target_source not in valid_sources:
        stream_request_validator.message = "Bad request"
        stream_request_validator.error = "Invalid source parameter"
        return stream_request_validator.bad_request()

    if find_all:
        stream_request_validator.params = {'find_all': find_all}
    else:
        stream_request_validator.params = {'location': location}

    return stream_request_validator.valid_request()


def stream_cache_key(validated_request):

    return None


def stream_db_key(validated_request):
    return None


def stream_aggregator_endpoint(validated_request):

    try:
        validated_request.data = EarthCamAggregator(provider=validated_request.target_source) \
            .get_streams(location=validated_request.params['location'])
    except KeyError:
        validated_request.data = EarthCamAggregator(provider=validated_request.target_source) \
            .get_all_streams()

    if validated_request.data is None:
        validated_request.message = "Error retrieving streams"
        validated_request.error = "Failed to retrieve location stream data"
        return validated_request.internal_server_error()

    return validated_request
