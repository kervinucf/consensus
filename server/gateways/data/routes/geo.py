from flask import Blueprint, request
from server.lib.objects.consensus_response import ConsensusResponse

from server.gateways.data.resources.providers.geo.request_handlers.find_countries \
    import validate_country_request, country_cache_key, country_db_key, country_aggregator_endpoint

from server.gateways.data.resources.providers.geo.request_handlers.find_cities \
    import validate_city_request, city_cache_key, city_db_key, city_aggregator_endpoint

from server.gateways.data.resources.providers.geo.request_handlers.find_coordinates \
    import validate_coordinates_request, coordinates_cache_key, coordinates_db_key, coordinates_aggregator_endpoint

from server.gateways.data.resources.providers.geo.request_handlers.find_distance \
    import validate_distance_request, distance_cache_key, distance_db_key, distance_aggregator_endpoint

geo = Blueprint('geo', __name__, url_prefix="/geo")


# ######################################################################################################################
# LIVE ENDPOINTS     ###################################################################################################

# Description:
# List all countries on earth
# Return country based on input
# Same goes for cities
# Return coordinates based on input
# Get distance between two
# ######################################################################################################################


@geo.route("/countries", methods=["POST"])
def find_countries():
    consensus_response = ConsensusResponse()
    request_to_be_fufilled = validate_country_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = country_cache_key
    consensus_response.db_key = country_db_key
    consensus_response.api_endpoint = country_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response


@geo.route("/cities", methods=["POST"])
def find_cities():
    consensus_response = ConsensusResponse()
    request_to_be_fufilled = validate_city_request(request)
    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = city_cache_key
    consensus_response.db_key = city_db_key
    consensus_response.api_endpoint = city_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response


# find city by name


@geo.route("/coordinates", methods=["POST"])
def find_coordinatesd(location=None):
    consensus_response = ConsensusResponse()
    request_to_be_fufilled = validate_coordinates_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = coordinates_cache_key
    consensus_response.db_key = coordinates_db_key
    consensus_response.api_endpoint = coordinates_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response


@geo.route("/distance", methods=["POST"])
def find_distance():
    consensus_response = ConsensusResponse()
    request_to_be_fufilled = validate_distance_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = distance_cache_key
    consensus_response.db_key = distance_db_key
    consensus_response.api_endpoint = distance_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response
