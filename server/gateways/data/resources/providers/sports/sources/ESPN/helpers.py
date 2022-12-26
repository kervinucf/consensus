from server.gateways.data.resources.providers.sports.sources.ESPN.utils import League
import requests


def complete_request(url, bearer_oauth=None, params=None, bypassing=False):
    # add espn gateways ratelimits - check_rate_limit | REMOVE 12, 13 HASHTAGS TO CHECK RATELIMIT |

    def connect_to_url(url, bearer_oauth=None, params=None):
        return requests.request("GET", url, auth=bearer_oauth, json=params)

    response = connect_to_url(url, bearer_oauth, params)
    if response.status_code != 200:
        return {
            "status": "failed",
            "error": response.text,
            "code": response.status_code
        }
    else:
        return {
            "status": "success",
            "res": response.json()
        }


def get_url(sport, league):
    return f'http://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard'


def sports_leagues(sport):
    if sport:
        return sports_leagues()[sport]

    return {
        "basketball": "nba",
        "baseball": "mlb",
        "football": "nfl",
        "soccer": ['usa.1', 'eng.1', 'eng.2', 'eng.3', 'eng.4', 'eng.5', 'esp.1', 'esp.2', 'ger.1', 'ger.2', 'fra.1',
                   'fra.2', 'tur.1', 'tur.2', 'ita.1', 'ita.2', 'fifa.world', 'uefa.champions']
    }


def EspnAPI(league, _id=None, ):
    league = league.lower()

    if league == 'nba':
        response = complete_request(url=get_url(
            sport="basketball", league="nba"), bypassing=True)
    if league == 'mlb':
        response = complete_request(url=get_url(
            sport="baseball", league="mlb"), bypassing=True)
    if league == 'nfl':
        response = complete_request(url=get_url(
            sport="football", league="nfl"), bypassing=True)

    soccer_leagues = ['usa.1', 'eng.1', 'eng.2', 'eng.3', 'eng.4', 'eng.5', 'esp.1', 'esp.2', 'ger.1', 'ger.2', 'fra.1',
                      'fra.2', 'tur.1', 'tur.2', 'ita.1', 'ita.2', 'fifa.world', 'uefa.champions']
    if league in soccer_leagues:
        response = complete_request(url=get_url(
            sport="soccer", league=league), bypassing=True)

    return League(response)
