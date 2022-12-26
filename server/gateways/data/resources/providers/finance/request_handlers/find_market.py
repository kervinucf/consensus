from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.finance.controller import FinanceAggregator


def validate_market_request(request):

    market_request_validator = RequestValidator()

    market = None
    detail = None

    try:
        market = request.get_json()['market']
        detail = request.get_json()['detail']
        market_request_validator.target_source = request.get_json()['source']
    except KeyError:
        pass

    if market is None:
        market_request_validator.message = "Bad request"
        market_request_validator.error = "Missing market parameter"
        return market_request_validator.bad_request()

    if detail is not None:
        valid_details = ["overview", "gainers", "losers", "most_active"]
        if detail not in valid_details:
            market_request_validator.message = "Bad request"
            market_request_validator.error = "Invalid detail parameter"
            return market_request_validator.bad_request()

    # valid_markets = []
    # source is optional
    valid_sources = ['yahoo']
    if market_request_validator.target_source is not None and market_request_validator.target_source not in valid_sources:
        market_request_validator.message = "Bad request"
        market_request_validator.error = "Invalid source parameter"
        return market_request_validator.bad_request()

    market_request_validator.params = {
        'market': market.upper(),
        'detail': detail.upper()
    }

    return market_request_validator.valid_request()


def market_cache_key(validated_request):
    return None


def market_db_key(validated_request):
    return None


def market_aggregator_endpoint(validated_request):
    validated_request.data = FinanceAggregator(provider=validated_request.target_source)\
        .get_markets(market=validated_request.params['market'], detail=validated_request.params["detail"])
    if validated_request.data is None:
        validated_request.message = "Error retrieving market data"
        validated_request.error = "Failed to retrieve market data"
        return validated_request.internal_server_error()

    return validated_request
