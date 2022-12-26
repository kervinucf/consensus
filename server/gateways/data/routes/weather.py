from flask import Blueprint, request
from server.lib.objects.consensus_response import ConsensusResponse

from server.gateways.data.resources.providers.weather.request_handlers.find_forecast \
    import validate_forecast_request, forecast_cache_key, forecast_db_key, forecast_aggregator_endpoint

from server.gateways.data.resources.providers.weather.request_handlers.find_day_night_phases \
    import validate_day_night_phases_request, day_night_phases_cache_key, day_night_phases_db_key,\
    day_night_phases_aggregator_endpoint


from server.gateways.data.resources.providers.weather.request_handlers.find_earthquakes\
    import validate_earthquake_request, earthquake_cache_key, earthquake_db_key, earthquake_aggregator_endpoint

weather = Blueprint('weather', __name__, url_prefix="/weather")

# weather.register_endpoint(espn)


@weather.route("/forecasts", methods=["POST"])
def find_forecasts():
    consensus_response = ConsensusResponse()
    # params - location, source, timeframe
    # timeframes - extended, current, forecast
    request_to_be_fufilled = validate_forecast_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = forecast_cache_key
    consensus_response.db_key = forecast_db_key
    consensus_response.api_endpoint = forecast_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response


@weather.route("/day_night_phases", methods=["POST"])
def find_day_night_phases():
    consensus_response = ConsensusResponse()
    request_to_be_fufilled = validate_day_night_phases_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = day_night_phases_cache_key
    consensus_response.db_key = day_night_phases_db_key
    consensus_response.api_endpoint = day_night_phases_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response


@weather.route("/earthquakes", methods=["GET", "POST"])
def find_earthquakes():
    consensus_response = ConsensusResponse()
    request_to_be_fufilled = validate_earthquake_request(request)

    if request_to_be_fufilled.expected_status_code != 200:
        return consensus_response.return_bad_request(req=request_to_be_fufilled)

    consensus_response.cache_key = earthquake_cache_key
    consensus_response.db_key = earthquake_db_key
    consensus_response.api_endpoint = earthquake_aggregator_endpoint

    fufilled_response = consensus_response.fufill_request(
        req=request_to_be_fufilled)

    return fufilled_response
