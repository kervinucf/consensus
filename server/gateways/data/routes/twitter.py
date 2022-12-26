from flask import Blueprint, request
from server.lib.objects.consensus_response import ConsensusResponse

from server.gateways.data.resources.providers.twtr.request_handlers.find_user \
    import validate_user_request, user_cache_key, user_db_key, user_aggregator_endpoint

from server.gateways.data.resources.providers.twtr.request_handlers.find_tweets \
    import validate_tweets_request, tweets_cache_key, tweets_db_key, tweets_aggregator_endpoint

from server.gateways.data.resources.providers.twtr.request_handlers.find_spaces \
    import validate_spaces_request, spaces_cache_key, spaces_db_key, spaces_aggregator_endpoint

from server.gateways.data.resources.providers.twtr.request_handlers.find_trends \
    import validate_trends_request, trends_cache_key, trends_db_key, trends_aggregator_endpoint

twitter = Blueprint('twitter', __name__, url_prefix="/twitter")


# twitter.register_endpoint(espn)

# find tweeter information
@twitter.route("/users", methods=["POST"])
def find_user():
    consensus_response = ConsensusResponse()
    # params = user_name
    request_to_be_fufilled = validate_user_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = user_cache_key
    consensus_response.db_key = user_db_key
    consensus_response.api_endpoint = user_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response


# find spaces by term
@twitter.route("/spaces", methods=["POST"])
def find_spaces():
    consensus_response = ConsensusResponse()
    # params = space_id, search_term, or top
    request_to_be_fufilled = validate_spaces_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = spaces_cache_key
    consensus_response.db_key = spaces_db_key
    consensus_response.api_endpoint = spaces_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response


@twitter.route("/tweets", methods=["POST"])
def find_tweets():
    consensus_response = ConsensusResponse()
    # params = tweet_id, search_term, user, count
    request_to_be_fufilled = validate_tweets_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = tweets_cache_key
    consensus_response.db_key = tweets_db_key
    consensus_response.api_endpoint = tweets_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response


@twitter.route("/trends", methods=["GET", "POST"])
def find_global_trends():
    consensus_response = ConsensusResponse()
    # params = world_wide, global, or place
    request_to_be_fufilled = validate_trends_request(request)
    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = trends_cache_key
    consensus_response.db_key = trends_db_key
    consensus_response.api_endpoint = trends_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response
