from npc_network_news.backend.lib.Redis.resources import publish, subscribe, get_redis
from lib.Twitter.snowflake.helpers import get_stream_channel


def unfiltered_stream(response):
    # ......................................................
    # CLEAN TWEET OBJECT

    # ......................................................

    # publish to main stream
    publish_to_stream(content=response)


def publish_tweet_to_stream(tweet, tag=None):
    if tag:
        publish_to_stream(tweet, stream=tag)

    publish_to_stream(tweet)

# ......................................................


def publish_to_stream(content, stream=get_stream_channel()):
    # stuff
    publish(redis=get_redis(), channel=stream, content=content)


def subscribe_to_stream(web_socket, stream=get_stream_channel()):

    def broadcast(message):
        if message and not message['data'] == 1:
            if message['types'] == 'message':
                web_socket.send(message)

    subscribe(redis=get_redis(), channel=stream, message_handler=broadcast)
