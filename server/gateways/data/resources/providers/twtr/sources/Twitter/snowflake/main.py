from utils import firehose
import time
from lib.Twitter.api import lookup_tweets
from lib.Twitter.api import get_current_time
from lib.Twitter.events.setup import setup_event_handlers
from lib.Events.event_controller import post_event


# ......................................................
def find_tweets(id_list):
    post_event("unfiltered tweet found", lookup_tweets(id_list))
# ......................................................


def run():

    fh = firehose()
    setup_event_handlers()

    while True:
        try:
            start = int(get_current_time() * 1000) - \
                1000  # Start from current time
            end = start + 5000  # Get five seconds of the timeline
            fh.ingest_range(start, end, processor=find_tweets)
        except Exception as e:
            status_logger(non_status_text=e)
            time.sleep(60)


run()
