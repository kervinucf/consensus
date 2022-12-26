from flask import Blueprint, request
from server.lib.objects.consensus_response import ConsensusResponse

from server.gateways.data.resources.providers.sports.request_handlers.find_events \
    import validate_event_request, event_cache_key, event_db_key, event_aggregator_endpoint

from server.gateways.data.resources.providers.sports.request_handlers.find_leagues \
    import validate_league_request, league_cache_key, league_db_key, league_aggregator_endpoint

sports = Blueprint('sports', __name__, url_prefix="/sports")


# sports.register_endpoint(espn)


# ######################################################################################################################
# LIVE ENDPOINTS     ###################################################################################################

# Description:
#
# ######################################################################################################################


@sports.route("/leagues", methods=["POST"])
def find_leagues():
    consensus_response = ConsensusResponse()
    request_to_be_fufilled = validate_league_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = league_cache_key
    consensus_response.db_key = league_db_key
    consensus_response.api_endpoint = league_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response


@sports.route("/events", methods=["POST"])
def find_events():
    consensus_response = ConsensusResponse()
    request_to_be_fufilled = validate_event_request(request)
    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = event_cache_key
    consensus_response.db_key = event_db_key
    consensus_response.api_endpoint = event_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response

# _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
