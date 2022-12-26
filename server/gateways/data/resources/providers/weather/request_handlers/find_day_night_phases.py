from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.weather.controller import WeatherAggregator


def validate_day_night_phases_request(request):
    day_night_phases_request_validator = RequestValidator()

    try:
        location = request.get_json()["location"]
    except KeyError:
        location = None

    try:
        timezone = request.get_json()["timezone"]
    except KeyError:
        timezone = None

    if location is None and timezone is None:
        day_night_phases_request_validator.message = "Bad request"
        day_night_phases_request_validator.error = "Missing location and timezone parameters"
        return day_night_phases_request_validator.bad_request()

    if location is not None and timezone is not None:
        day_night_phases_request_validator.message = "Bad request"
        day_night_phases_request_validator.error = "Both location and timezone parameters were specified"
        return day_night_phases_request_validator.bad_request()

    try:
        sun_phases = request.get_json()["sun_phases"]
    except KeyError:
        sun_phases = False

    try:
        moon_phases = request.get_json()["moon_phases"]
    except KeyError:
        moon_phases = False

    if not sun_phases and not moon_phases:
        day_night_phases_request_validator.message = "Bad request"
        day_night_phases_request_validator.error = "Missing sun_phases and moon_phases parameters"
        return day_night_phases_request_validator.bad_request()

    if sun_phases and moon_phases:
        day_night_phases_request_validator.message = "Bad request"
        day_night_phases_request_validator.error = "Both sun_phases and moon_phases parameters were specified"
        return day_night_phases_request_validator.bad_request()

    try:
        day_night_phases_request_validator.target_source = request.get_json()[
            "source"]
    except KeyError:
        pass

    if day_night_phases_request_validator.target_source is not None and day_night_phases_request_validator.target_source not in [
            "weather"]:
        day_night_phases_request_validator.message = "Bad request"
        day_night_phases_request_validator.error = "Invalid source parameter"
        return day_night_phases_request_validator.bad_request()

    day_night_phases_request_validator.params = {"location": location,
                                           "timezone": timezone,
                                           "sun_phases": sun_phases,
                                           "moon_phases": moon_phases}

    return day_night_phases_request_validator.valid_request()


def day_night_phases_cache_key(validated_request):
    return None


def day_night_phases_db_key(validated_request):
    return None


def day_night_phases_aggregator_endpoint(validated_request):

    sun_phases = False
    moon_phases = False

    if validated_request.params["sun_phases"]:
        sun_phases = True
    if validated_request.params["moon_phases"]:
        moon_phases = True

    if validated_request.params["location"]:
        if sun_phases:
            validated_request.data = WeatherAggregator(provider=validated_request.target_source)\
                .get_sun_phases(location=validated_request.params['location'])
        if moon_phases:
            validated_request.data = WeatherAggregator(provider=validated_request.target_source)\
                .get_moon_phases(location=validated_request.params['location'])

    if validated_request.params["timezone"]:
        if sun_phases:
            validated_request.data = WeatherAggregator(provider=validated_request.target_source)\
                .get_sun_phases(timezone=validated_request.params['timezone'])
        if moon_phases:
            validated_request.data = WeatherAggregator(provider=validated_request.target_source)\
                .get_moon_phases(timezone=validated_request.params['timezone'])

    if validated_request.data is None:
        if sun_phases:
            validated_request.message = "Error retrieving sun_phases"
            validated_request.error = "Failed to retrieve sun_phases"
        if moon_phases:
            validated_request.message = "Error retrieving moon_phases"
            validated_request.error = "Failed to retrieve moon_phases"

        return validated_request.internal_server_error()

    return validated_request
