from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.twtr.controller import TwitterAggregator


def validate_trends_request(request):

    trends_request_validator = RequestValidator()

    try:
        worldwide = request.get_json()['worldwide']
    except TypeError:
        worldwide = None
    except KeyError:
        worldwide = None

    try:
        _global = request.get_json()['global']
    except TypeError:
        _global = None
    except KeyError:
        _global = None

    try:
        place = request.get_json()['place']
    except TypeError:
        place = None
    except KeyError:
        place = None

    if worldwide is None and _global is None and place is None:
        trends_request_validator.message = "Bad request"
        trends_request_validator.error = "Missing worldwide, global, or place parameter"
        return trends_request_validator.bad_request()

    if worldwide and _global or worldwide and place or _global and place or worldwide and _global and place:
        trends_request_validator.message = "Bad request"
        trends_request_validator.error = "Only one of worldwide, global, or place parameter allowed"
        return trends_request_validator.bad_request()

    trends_request_validator.params = {
        'worldwide': worldwide,
        'global': _global,
        'place': place
    }

    return trends_request_validator.valid_request()


def trends_cache_key(validated_request):
    return None


def trends_db_key(validated_request):
    return None


def trends_aggregator_endpoint(validated_request):

    if validated_request.params['worldwide']:
        validated_request.data = TwitterAggregator() \
            .find_trends(location='Worldwide')
    elif validated_request.params['global']:
        validated_request.data = TwitterAggregator() \
            .find_trends(_global=True)
    elif validated_request.params['place']:
        validated_request.data = TwitterAggregator() \
            .find_trends(location=validated_request.params['place'])

    if validated_request.data is None:
        validated_request.message = "Error retrieving trend data"
        validated_request.error = "Failed to retrieve trend data"
        return validated_request.internal_server_error()

    return validated_request
