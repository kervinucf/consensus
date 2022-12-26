from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.sports.controller import SportsAggregator


def validate_league_request(request):
    league_request_validator = RequestValidator()
    sport = None
    find_all = False

    try:
        sport = request.get_json()['sport']
    except KeyError:
        find_all = request.get_json()['find_all']

    try:
        league_request_validator.target_source = request.get_json()['source']
    except KeyError:
        pass

    if sport is None and find_all is False:
        league_request_validator.message = "Bad request"
        league_request_validator.error = "Missing sport parameter"
        return league_request_validator.bad_request()

    if sport is not None and find_all is True:
        league_request_validator.message = "Bad request"
        league_request_validator.error = "Cannot use both sport and find_all parameters"
        return league_request_validator.bad_request()

    if sport is not None and sport not in [
        "baseball",
        "basketball",
        "football",
        "hockey",
        "soccer",
    ]:
        league_request_validator.message = "Bad request"
        league_request_validator.error = "Invalid sport parameter"
        return league_request_validator.bad_request()

        # source is optional
    valid_sources = ['espn']
    if league_request_validator.target_source is not None and league_request_validator.target_source not in valid_sources:
        league_request_validator.message = "Bad request"
        league_request_validator.error = "Invalid source parameter"
        return league_request_validator.bad_request()

    if sport is not None:
        league_request_validator.params = {'sport': sport}
    else:
        league_request_validator.params = {'find_all': find_all}

    return league_request_validator.valid_request()


def league_cache_key(validated_request):
    return None


def league_db_key(validated_request):
    return None


def league_aggregator_endpoint(validated_request):
    try:
        validated_request.data = SportsAggregator(provider=validated_request.target_source) \
            .get_league(sport=validated_request.params['sport'])
    except KeyError:
        validated_request.data = SportsAggregator(
            provider=validated_request.target_source).get_leagues()

    if validated_request.data is None:
        validated_request.message = "Error retrieving league data"
        validated_request.error = "Failed to retrieve league data"
        return validated_request.internal_server_error()

    return validated_request
