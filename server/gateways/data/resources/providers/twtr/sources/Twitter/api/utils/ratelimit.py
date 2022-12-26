from server.lib.utils.database import get_from_db, update_record, save_to_db, get_db
import re
import time
from server.lib.utils.logger import status_logger


def get_current_time():
    return time.time()


def enforce_ratelimit(endpoint):
    status_logger(non_status_text="RATELIMIT EXCEEDED -> ",
                  status_text=f"{endpoint}", red=True)
    # check reset
    limited_endpoint_info = get_from_db(
        get_db('TwitterDatabase'), 'RateLimit', {'gateways': endpoint})
    time_to_reset = limited_endpoint_info['reset']
    if time_to_reset is not None:
        now = get_current_time()
        if not rate_exceeded(expected=time_to_reset, actual=now):
            time_left = time_to_reset - now
            status_logger(
                non_status_text='{} seconds left until rate limit resets!'.format(time_left))
            return limited_endpoint_info
        else:
            return init_rate_limit(endpoint=endpoint)
    else:
        status_logger(non_status_text='no reset time yet added')
        return rate_limit_endpoint(endpoint)


def rate_limit_endpoint(endpoint):
    # list of all gateways
    endpoint_limit_info = {
        'gateways': endpoint,
        'reset': get_current_time() + (15 * 60),
        'ratelimited': True,
        # get_rate_limit(gateways='exampleEndpoint, _type='exampleEndpointType'):
        'max': get_rate_limit(endpoint),
        'current': 0,
        'first_accessed': None
    }
    status_logger(non_status_text='updating rate limited info in db')
    update_record(get_db('TwitterDatabase'), 'RateLimit',
                  {'gateways': endpoint}, endpoint_limit_info)
    return endpoint_limit_info


def init_rate_limit(endpoint=None):
    # list of all gateways
    endpoint_limit_info = {
        'gateways': endpoint,
        'reset': None,
        'ratelimited': False,
        # get_rate_limit(gateways='exampleEndpoint, _type='exampleEndpointType'):
        'max': get_rate_limit(endpoint),
        'current': 0,
        'first_accessed': None
    }
    status_logger(
        non_status_text='saving to new gateways rate limit info to db')
    save_to_db(get_db('TwitterDatabase'), 'RateLimit', endpoint_limit_info)
    return endpoint_limit_info


def get_rate_limit(endpoint):
    # get limits for all gateways
    # update _type later when adding user/tweet context gateways
    endpoint_info = endpoint.split('-')
    context = endpoint_info[0]
    _type = endpoint_info[1]
    if _type == 'lookup':
        if context == 'conversation':
            return 900
        if context == 'users':
            return 900
        if context == 'spaces':
            return 300
        if context == 'trends':
            return 75
    if _type == 'recent':
        if context == 'conversation':
            return 180


def rate_exceeded(expected, actual):
    limit_remaining = expected - actual
    if limit_remaining > 0:
        return False
    else:
        return True


def get_endpoint(url):
    action = 'lookup'
    status_logger(non_status_text=url)

    try:
        try:
            endpoint = re.findall('2/(.+?)\?', url)[0]
        except IndexError:
            slashes = url.split('/')
            if 'recent' in slashes:
                action = 'recent'
            endpoint = re.findall('2/(.+?)/', url)[0]
    except IndexError:
        try:
            endpoint = re.findall('2/(.+?)', url)[0]
        except IndexError:
            endpoint = re.findall('1\.1/(.+?)/', url)[0]
    # https://api.twitter.com/2/tweets

    # get gateways action from url, action = 'look up' for now
    return '{}-{}'.format(endpoint, action)


def check_rate_limit(url):
    endpoint = get_endpoint(url)

    try:
        rate_limit_info = get_from_db(
            get_db('TwitterDatabase'), 'RateLimit', {'gateways': endpoint})
    except TypeError:
        return update_rate_limit_status(init_rate_limit(endpoint=endpoint))
    status_logger(non_status_text=rate_limit_info)
    if rate_limit_info['ratelimited']:
        if rate_limit_info['first_accessed']:
            time_diff = rate_limit_info['first_accessed'] - get_current_time()
            if rate_exceeded(expected=15 * 60, actual=time_diff):
                return update_rate_limit_status(init_rate_limit(endpoint=endpoint))

        if not rate_exceeded(expected=rate_limit_info['max'], actual=rate_limit_info['current'] + 1):
            return update_rate_limit_status(rate_limit_info)
        else:
            # next request will exceed limit
            status_logger(non_status_text='over request limit')
            return update_rate_limit_status(enforce_ratelimit(endpoint))
    else:
        return update_rate_limit_status(enforce_ratelimit(endpoint))


def update_rate_limit_status(rate_limit_status):
    if rate_limit_status['ratelimited']:
        return {
            'ratelimited': True,
            'error': rate_limit_status
        }
    if rate_limit_status['first_accessed'] is None:
        rate_limit_status['first_accessed'] = get_current_time()
    rate_limit_status.update(
        {'current': rate_limit_status['current'] + 1})
    update_record(get_db('TwitterDatabase'), 'RateLimit', {
        'gateways': rate_limit_status['gateways']}, rate_limit_status)
    return {
        'ratelimited': False,
        'error': rate_limit_status
    }
