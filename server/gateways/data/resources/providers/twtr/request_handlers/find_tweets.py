from server.lib.objects.validator import RequestValidator
from server.gateways.data.resources.providers.twtr.controller import TwitterAggregator


def validate_tweets_request(request):
    tweets_request_validator = RequestValidator()

    try:
        tweet_id = request.get_json()['tweet_id']
    except KeyError:
        tweet_id = False

    try:
        search_term = request.get_json()['search_term']
    except KeyError:
        search_term = False

    try:
        user = request.get_json()['user']
    except KeyError:
        user = False

    try:
        count = request.get_json()['count']
    except KeyError:
        count = 10

    if tweet_id is False and search_term is False and user is False:
        tweets_request_validator.message = "Bad request"
        tweets_request_validator.error = "Missing tweet_id, search_term, or user parameter"
        return tweets_request_validator.bad_request()

    if tweet_id and search_term or tweet_id and user or search_term and user or tweet_id and search_term and user:
        tweets_request_validator.message = "Bad request"
        tweets_request_validator.error = "Only one of tweet_id, search_term, or user parameter allowed"
        return tweets_request_validator.bad_request()

    tweets_request_validator.params = {
        'tweet_id': tweet_id,
        'search_term': search_term,
        'user': user,
        'max_results': count
    }

    return tweets_request_validator.valid_request()


def tweets_cache_key(validated_request):
    return None


def tweets_db_key(validated_request):
    return None


def tweets_aggregator_endpoint(validated_request):

    if validated_request.params['tweet_id']:
        validated_request.data = TwitterAggregator() \
            .find_tweets(_id_list=[validated_request.params['tweet_id']], max_results=validated_request.params['max_results'])
    elif validated_request.params['search_term']:
        validated_request.data = TwitterAggregator() \
            .find_tweets(search_term=validated_request.params['search_term'], max_results=validated_request.params['max_results'])
    elif validated_request.params['user']:
        validated_request.data = TwitterAggregator() \
            .find_tweets(username=validated_request.params['user'], max_results=validated_request.params['max_results'])

    if validated_request.data is None:
        validated_request.message = "Error retrieving tweet data"
        validated_request.error = "Failed to retrieve tweet data"
        return validated_request.internal_server_error()

    return validated_request
