from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.weather.controller import WeatherAggregator


def validate_earthquake_request(request):
    earthquake_request_validator = RequestValidator()

    try:
        earthquake_request_validator.target_source = request.get_json()[
            "source"]
    except TypeError:
        pass
    except KeyError:
        pass

    if earthquake_request_validator.target_source is not None and earthquake_request_validator.target_source not in [
            "weather"]:
        earthquake_request_validator.message = "Bad request"
        earthquake_request_validator.error = "Invalid source parameter"
        return earthquake_request_validator.bad_request()

    return earthquake_request_validator.valid_request()


def earthquake_cache_key(validated_request):
    return None


def earthquake_db_key(validated_request):
    return None


def earthquake_aggregator_endpoint(validated_request):
    validated_request.data = WeatherAggregator(
        provider=validated_request.target_source).get_earthquakes()
    if validated_request.data is None:
        validated_request.message = "Error retrieving earthquakes"
        validated_request.error = "Failed to retrieve earthquakes"
        return validated_request.internal_server_error()

    return validated_request
