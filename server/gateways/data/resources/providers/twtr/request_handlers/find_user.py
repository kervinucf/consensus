from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.twtr.controller import TwitterAggregator


def validate_user_request(request):
    user_request_validator = RequestValidator()
    user_name = None

    try:
        user_name = request.get_json()['user_name']
    except KeyError:
        pass

    if user_name is None:
        user_request_validator.message = "Bad request"
        user_request_validator.error = "Missing user_name parameter"
        return user_request_validator.bad_request()
    else:
        user_request_validator.params = {'user_name': user_name}
        return user_request_validator.valid_request()


def user_cache_key(validated_request):
    return None


def user_db_key(validated_request):
    return None


def user_aggregator_endpoint(validated_request):
    validated_request.data = TwitterAggregator() \
        .find_user(user_name=validated_request.params['user_name'])
    if validated_request.data is None:
        validated_request.message = "Error retrieving user data"
        validated_request.error = "Failed to retrieve user data"
        return validated_request.internal_server_error()

    return validated_request
