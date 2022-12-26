from flask import Blueprint, request
from server.lib.objects.consensus_response import ConsensusResponse

from server.gateways.data.resources.providers.earthcam.request_handlers.find_available_streams \
    import validate_stream_request, stream_cache_key, stream_db_key, stream_aggregator_endpoint

cams = Blueprint('cams', __name__, url_prefix="/cams")

# ######################################################################################################################
# LIVE ENDPOINTS     ###################################################################################################

# Description:
# List all endpoints for earth cams on youtube
# Search closest endpoints based on location input
# ######################################################################################################################


@cams.route("/streams", methods=["GET", "POST"])
def find_available_streams():
    consensus_response = ConsensusResponse()
    # valid params: location, source
    request_to_be_fufilled = validate_stream_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = stream_cache_key
    consensus_response.db_key = stream_db_key
    consensus_response.api_endpoint = stream_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response
