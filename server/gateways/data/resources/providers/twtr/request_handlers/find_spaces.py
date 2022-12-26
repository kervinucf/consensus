from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.twtr.controller import TwitterAggregator


def validate_spaces_request(request):

    spaces_request_validator = RequestValidator()

    try:
        space_id = request.get_json()['space_id']
    except KeyError:
        space_id = None

    try:
        search_term = request.get_json()['search_term']
    except KeyError:
        search_term = None

    try:
        top = request.get_json()['top']
    except KeyError:
        top = None

    if space_id is None and search_term is None and top is None:
        spaces_request_validator.message = "Bad request"
        spaces_request_validator.error = "Missing space_id, search_term, or top parameter"
        return spaces_request_validator.bad_request()

    if space_id and search_term or space_id and top or search_term and top or space_id and search_term and top:
        spaces_request_validator.message = "Bad request"
        spaces_request_validator.error = "Only one of space_id, search_term, or top parameter allowed"
        return spaces_request_validator.bad_request()

    spaces_request_validator.params = {
        'space_id': space_id,
        'search_term': search_term,
        'top': top
    }

    return spaces_request_validator.valid_request()


def spaces_cache_key(validated_request):
    return None


def spaces_db_key(validated_request):
    return None


def spaces_aggregator_endpoint(validated_request):

    if validated_request.params['space_id']:
        validated_request.data = TwitterAggregator() \
            .find_spaces(_id=[validated_request.params['space_id']])
    elif validated_request.params['search_term']:
        validated_request.data = TwitterAggregator() \
            .find_spaces(search_term=validated_request.params['search_term'])
    elif validated_request.params['top']:
        validated_request.data = TwitterAggregator() \
            .find_spaces(top=validated_request.params['top'])

    if validated_request.data is None:
        validated_request.message = "Error retrieving space data"
        validated_request.error = "Failed to retrieve space data"
        return validated_request.internal_server_error()

    return validated_request
