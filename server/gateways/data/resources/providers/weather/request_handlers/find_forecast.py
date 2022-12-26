from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.weather.controller import WeatherAggregator


def validate_forecast_request(request):
    forecast_request_validator = RequestValidator()
    location = None
    timeframe = None

    try:
        location = request.get_json()["location"]
    except KeyError:
        pass

    try:
        # extended - 5 day forecast
        # current - todays hourly forecast

        timeframe = request.get_json()["timeframe"]

    except KeyError:
        pass

    try:
        forecast_request_validator.target_source = request.get_json()["source"]
    except KeyError:
        pass

    if location is None:
        forecast_request_validator.message = "Bad request"
        forecast_request_validator.error = "Missing location parameter"
        return forecast_request_validator.bad_request()

    if timeframe is not None and timeframe not in ["extended", "current", "forecast"]:
        forecast_request_validator.message = "Bad request"
        forecast_request_validator.error = "Invalid timeframe parameter"
        return forecast_request_validator.bad_request()

    if forecast_request_validator.target_source is not None and forecast_request_validator.target_source not in ["weather"]:
        forecast_request_validator.message = "Bad request"
        forecast_request_validator.error = "Invalid source parameter"
        return forecast_request_validator.bad_request()

    forecast_request_validator.params = {
        "location": location,
        "timeframe":timeframe
    }

    return forecast_request_validator.valid_request()


def forecast_cache_key(validated_request):
    return None


def forecast_db_key(validated_request):
    return None


def forecast_aggregator_endpoint(validated_request):
    validated_request.data = WeatherAggregator(
        provider=validated_request.target_source).get_forecast(location=validated_request.params['location'],
                                                               timeframe=validated_request.params["timeframe"])
    if validated_request.data is None:
        validated_request.message = "Error retrieving forecast"
        validated_request.error = "Failed to retrieve forecast"
        return validated_request.internal_server_error()

    return validated_request
