import requests
from datetime import datetime, timedelta


def time_passed(last_update, expiration_time):
    #             last_updated = games_progressing['last_updated']

    if last_update is not None:
        if type(last_update) is not float:
            last_updated = last_update['last_updated']
        else:
            last_updated = last_update
        # if timestamp is expired...need to update games
        now = get_current_time()
        elapsed_time = now - last_updated

        # greater than 4 seconds -- update
        if elapsed_time > expiration_time:

            return True

    else:
        return True


def get_current_time(future=None, date=False):

    if date:
        return datetime.now().date()
    if future:
        return get_current_time() + timedelta(seconds=future).total_seconds()
    return datetime.utcnow().timestamp()








