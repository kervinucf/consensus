#!/usr/bin/env python3

from collections import deque, defaultdict


class firehose:

    # Read Credentials
    current_api = 0
    api_counter = 0
    failures = 0

    MACHINE_IDS = (375, 382, 361, 372, 364, 381, 376, 365, 363,
                   362, 350, 325, 335, 333, 342, 326, 327, 336, 347, 332)
    SNOWFLAKE_EPOCH = 1288834974657

    def __init__(self):
        self.queue = deque()
        self.fh = open("firehose_test.ndjson", "a+")
        self.ratelimit_reset = None
        self.ratelimit_remaining = None

    def get_creation_time(self, id):
        return ((id >> 22) + 1288834974657)

    def machine_id(self, id):
        return (id >> 12) & 0b1111111111

    def sequence_id(self, id):
        return id & 0b111111111111

    # This method is where the magic happens
    def ingest_range(self, begin, end, processor):
        for epoch in range(begin, end):  # Move through each millisecond
            time_component = (epoch - self.SNOWFLAKE_EPOCH) << 22
            for machine_id in self.MACHINE_IDS:  # Iterate over machine ids
                for sequence_id in [0]:  # Add more sequence ids as needed
                    twitter_id = time_component + \
                        (machine_id << 12) + sequence_id
                    self.queue.append(twitter_id)
                    if len(self.queue) >= 100:
                        ids_to_process = []
                        for i in range(0, 100):
                            ids_to_process.append(self.queue.popleft())
                        processor(ids_to_process)

    def process_ids(self, tweet_ids):
        # ##############################################################

        status_logger(
            non_status_text='\n ***** {} ***** \n'.format(len(tweet_ids)))
        """conversation = firehose.gateways[firehose.current_api].statuses_lookup(tweet_ids,tweet_mode='extended',trim_user=False,include_entities=True)
        if 'x-rate-limit-remaining' in firehose.gateways[firehose.current_api].last_response.headers:
            self.ratelimit_remaining = int(firehose.gateways[firehose.current_api].last_response.headers['x-rate-limit-remaining'])
        if 'x-rate-limit-reset' in firehose.gateways[firehose.current_api].last_response.headers:
            self.ratelimit_reset = int(firehose.gateways[firehose.current_api].last_response.headers['x-rate-limit-reset'])"""
        # ##############################################################

        """ tweets_processed = defaultdict(int)
        for tweet in conversation:
            tweet._json['retrieved_on'] = int(get_current_time())
            status_logger(non_status_text=json.dumps(tweet._json,sort_keys=True,ensure_ascii=True),file=self.fh)
            created_at = tweet._json['created_at']
            id = int(tweet._json['id'])
            status_logger(non_status_text=self.machine_id(id),self.get_creation_time(id),self.sequence_id(id))
            tweets_processed[self.get_creation_time(id)] += 1

        status_logger(non_status_text=self.ratelimit_remaining)
        if self.ratelimit_remaining <= 0:
            firehose.api_counter += 1
            firehose.current_api = firehose.api_counter % len(firehose.gateways)"""
