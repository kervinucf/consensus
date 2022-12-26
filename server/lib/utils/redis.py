from redis import Redis
from dotenv import load_dotenv
import os
from logging import getLogger
logger = getLogger(__name__)

load_dotenv()

REDIS_DB_URL = os.environ.get("REDIS_DB_URL")
REDIS_DB_PASSWORD = os.environ.get("REDIS_DB_PASSWORD")


def get_redis():
    return Redis()


def get_redis2():
    return Redis(host=REDIS_DB_URL,
                 port=6379,
                 db=0,
                 password=REDIS_DB_PASSWORD,
                 socket_timeout=None,
                 connection_pool=None,
                 charset='utf-8',
                 errors='strict',
                 unix_socket_path=None)


def publish(redis, channel, content):
    redis.publish(channel, content)


def subscribe(redis, channel, message_handler):
    subscriber = redis.pubsub()
    subscriber.subscribe(channel)
    while True:
        if message_handler(subscriber.get_message()):
            continue
        else:
            break


def handler(message):
    if message and not message['data'] == 1:
        if message['types'] == 'message':
            logger.info('Message received: {}'.format(message['data']))
