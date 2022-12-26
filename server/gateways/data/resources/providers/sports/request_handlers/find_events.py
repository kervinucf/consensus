from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.sports.controller import SportsAggregator


def validate_event_request(request):
    event_request_validator = RequestValidator()
    league = None
    status = None

    try:
        league = request.get_json()['league']
        status = request.get_json()['status']
        event_request_validator.target_source = request.get_json()['source']
    except KeyError:
        pass

    if league is None:
        event_request_validator.message = "Bad request"
        event_request_validator.error = "Missing league parameter"
        return event_request_validator.bad_request()

    if status is not None and status not in ["scoreboard", "scheduled", "in_progress", "completed", "close"]:
        event_request_validator.message = "Bad request"
        event_request_validator.error = "Invalid status parameter"
        return event_request_validator.bad_request()

    # source is optional
    valid_sources = ['espn']
    if event_request_validator.target_source is not None and event_request_validator.target_source not in valid_sources:
        event_request_validator.message = "Bad request"
        event_request_validator.error = "Invalid source parameter"
        return event_request_validator.bad_request()

    event_request_validator.params = {'league': league, 'status': status}

    return event_request_validator.valid_request()


def event_cache_key(validated_request):
    return None


def event_db_key(validated_request):
    return None


def event_aggregator_endpoint(validated_request):
    validated_request.data = SportsAggregator(provider=validated_request.target_source)\
        .get_events(league=validated_request.params['league'],
                    status=validated_request.params['status'])
    if validated_request.data is None:
        validated_request.message = "Error retrieving event data"
        validated_request.error = "Failed to retrieve event data"
        return validated_request.internal_server_error()

    return validated_request
