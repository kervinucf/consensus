from server.gateways.data.resources.providers.twtr.sources.Twitter.api.utils.bearer import bearer_oauth

import requests
import re


def get_original_twitter_url(twitter_url):
    # without masking it as a browser request, it wont work properly
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url=twitter_url, headers=headers)
    data = r.text
    url = re.search("(?P<url>https?://[^\s]+)\"", data).group("url")
    return url


def create_rule(rule, tag=None):
    if tag is None:
        return {
            'value': rule,
            'tag': rule
        }
    return {
        'value': rule,
        'tag': tag
    }


def get_rules():
    print('getting current rules from gateways')

    url = "https://api.twitter.com/2/tweets/search/stream/rules"

    return {
        'url': url,
        'params': None,
        'headers': bearer_oauth,
        "GET": True
    }


def delete_rules(filter_ids=[]):
    print('deleting rules from gateways-> ', filter_ids)
    """
        if all:
        rules = get_rules()['res']
        print(rules)
        if rules['meta']['result_count'] > 0:
            filter_ids = list(map(lambda rule: rule['id'], rules['data']))
            delete_rules(filter_ids)
        else:
            return None
    """

    params = {"delete": {"ids": filter_ids}}

    url = "https://api.twitter.com/2/tweets/search/stream/rules"

    return {
        'url': url,
        'params': params,
        'headers': bearer_oauth,
        "GET": False
    }


def set_rules(rule_set):
    print('setting rules to gateways-> ', rule_set)
    params = {"add": rule_set[:20]}
    url = "https://api.twitter.com/2/tweets/search/stream/rules"
    return {
        'url': url,
        'params': params,
        'headers': bearer_oauth,
        "GET": False
    }
