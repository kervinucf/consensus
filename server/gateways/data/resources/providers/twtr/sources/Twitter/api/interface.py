import time
import requests
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.utils.ratelimit import check_rate_limit
from server.lib.utils.logger import status_logger

from server.gateways.data.resources.providers.twtr.sources.Twitter.api.entities.tweet import TweetEntity
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.entities.trend import PlaceEntity
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.entities.space import SpaceEntity
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.entities.rule import RuleEntity
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.entities.user import UserEntity


def complete_request(url, GET, bearer_oauth=None, params=None, bypassing=True):
    # add espn gateways ratelimits - check_rate_limit | REMOVE 12, 13 HASHTAGS TO CHECK RATELIMIT |

    def connect_to_url(url, GET, bearer_oauth=None, params=None):
        if GET:
            return requests.request("GET", url, auth=bearer_oauth, params=params)
        else:
            return requests.request("POST", url, auth=bearer_oauth, json=params)

    if not bypassing:
        rate_limit_info = check_rate_limit(url)

    if bypassing or not rate_limit_info["ratelimited"]:
        response = connect_to_url(url, GET, bearer_oauth, params)
        if response.status_code != 200 and response.status_code != 201:
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
    else:
        return {
            "status": "failed",
            "error": "ratelimited",
            "info": rate_limit_info
        }


def TwitterInterface(endpoint_creator, parameters=None, stream=False, tweet_endpoint=False,
                     space_endpoint=False,
                     trend_endpoint=False,
                     rule_endpoint=False,
                     user_endpoint=False,
                     num_results=None):

    if stream:
        message_handler = parameters
        for response in endpoint_creator().iter_lines():
            if response:
                message_handler(response)
            else:
                status_logger(non_status_text="no response found", red=True)
    else:
        if parameters:
            if num_results:
                if num_results < 10:
                    num_results = 10

                if num_results > 100:
                    num_results = 100

                endpoint = endpoint_creator(parameters, num_results)
            else:
                endpoint = endpoint_creator(parameters)
        else:
            endpoint = endpoint_creator()

        response = complete_request(
            url=endpoint["url"],
            bearer_oauth=endpoint["headers"],
            params=endpoint["params"],
            GET=endpoint["GET"],
        )

        def check_included(included, includes):
            if included:
                try:
                    return included[includes]
                except KeyError:
                    return None

        if response["status"] == "success":

            try:
                response_included = response['res']["includes"]
            except TypeError:
                response_included = None
            except KeyError:
                response_included = None

            try:
                response_meta = response['res']["meta"]
                result_count = response_meta["result_count"]
                if result_count == 0:
                    return None
            except TypeError:
                response_meta = None
            except KeyError:
                response_meta = None

            if tweet_endpoint:
                tweet_includes = response_included
                tweet_data_list = response["res"]["data"]

                tweets_found = []

                for tweet_data in tweet_data_list:

                    tweet_entity = TweetEntity(res_data=tweet_data)

                    if check_included(included=response_included, includes="users"):
                        tweet_entity.assign_roles(
                            users_included=tweet_includes["users"])

                    if check_included(included=response_included, includes="conversation"):
                        tweet_entity.read_tweet_chain(
                            tweets_included=tweet_includes["conversation"])
                    # order?
                    if check_included(included=response_included, includes="media"):
                        tweet_entity.add_media(
                            media_included=tweet_includes["media"])

                    if check_included(included=response_included, includes="places"):
                        tweet_entity.add_places(
                            places_included=tweet_includes["places"])

                    if check_included(included=response_included, includes="polls"):
                        tweet_entity.add_polls(
                            polls_included=tweet_includes["polls"])
                    tweets_found.append(tweet_entity)

                return tweets_found

            if space_endpoint:
                spaces_found = []
                space_data_list = response["res"]["data"]

                for space_data in space_data_list:
                    space_entity = SpaceEntity(res_data=space_data)

                    if check_included(included=response_included, includes="users"):
                        space_entity.assign_roles(
                            users_included=response_included["users"])

                    spaces_found.append(space_entity)

                return spaces_found

            if trend_endpoint:

                if response["res"]:
                    response = response["res"][0]
                    return PlaceEntity(res_data=response)

            if user_endpoint:
                user_data_list = response["res"]["data"]

                users_found = []

                for tweet_data in user_data_list:
                    user_entity = UserEntity(res_data=tweet_data)
                    users_found.append(user_entity)
                return users_found

            if rule_endpoint:

                if response["res"]:
                    return RuleEntity(res_data=response)
        else:
            return response["error"]
