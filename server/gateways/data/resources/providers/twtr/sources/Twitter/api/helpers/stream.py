from server.gateways.data.resources.providers.twtr.sources.Twitter.api.utils.bearer import bearer_oauth
import requests
from logging import getLogger
logger = getLogger(__name__)


def add_fields(url):
    url += '?'
    user_fields = '&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,' \
                  'protected,public_metrics,url,username,verified'
    tweet_fields = '&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,' \
                   'id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,' \
                   'source,text'
    poll_fields = '&poll.fields=duration_minutes,end_datetime,id,options,voting_status'
    place_fields = '&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type'
    media_fields = '&media.fields=duration_ms,height,media_key,preview_image_url,types,url,width,public_metrics,alt_text'
    expansions = '&expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,' \
                 'geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id'
    url += user_fields
    url += tweet_fields
    url += poll_fields
    url += place_fields
    url += media_fields
    url += expansions
    return url


def filtered_stream():
    url = "https://api.twitter.com/2/tweets/search/stream"

    res = requests.get(
        add_fields(url), auth=bearer_oauth, stream=True,
    )
    if res.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                res.status_code, res.text
            )
        )

    return res


def read_filtered_stream(cb):
    url = "https://api.twitter.com/2/tweets/search/stream"

    res = requests.get(
        add_fields(url), auth=bearer_oauth, stream=True,
    )

    if res.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                res.status_code, res.text
            )
        )

    read_stream(res, cb)


def read_stream(response, cb=None):

    for response_line in response.iter_lines():
        if response_line:
            cb(response_line)
        else:
            logger.debug(f'no response found {response_line}')
