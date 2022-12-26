from flask import Blueprint, request
from server.lib.objects.consensus_response import ConsensusResponse

from server.gateways.data.resources.providers.finance.request_handlers.find_market \
    import validate_market_request, market_cache_key, market_db_key, market_aggregator_endpoint

finance = Blueprint('finance', __name__, url_prefix="/finance")


# ######################################################################################################################
# LIVE ENDPOINTS     ###################################################################################################

# Description:
#
# ######################################################################################################################


@finance.route("/markets", methods=["GET", "POST"])
def find_market():
    consensus_response = ConsensusResponse()
    request_to_be_fufilled = validate_market_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = market_cache_key
    consensus_response.db_key = market_db_key
    consensus_response.api_endpoint = market_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response
