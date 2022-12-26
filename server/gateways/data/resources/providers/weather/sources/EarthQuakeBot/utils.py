import re
from dataclasses import dataclass
import datetime


@dataclass
class EarthQuake:

    def __init__(self, tweet):
        self.recent = False
        self.data = self.create_event(tweet)

    @staticmethod
    def get_time_since_event(begin_time):
        begin_time = datetime.datetime.strptime(begin_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        now = datetime.datetime.now()
        return (begin_time - now).total_seconds() / 60 / 60

    def create_event(self, tweet):
        message = tweet["tweet"]["content"]["text"]
        seconds_since = self.get_time_since_event(
            tweet["tweet"]["created_at"])
        # 'created_at'

        posted = (seconds_since / 60) / 60
        if posted < 12:
            self.recent = True
            regex = r"([0-9]\.[0-9]) magnitude"
            magnitude = re.findall(regex, message)
            coordinates = {
                'lat': tweet["tweet"]["geo"]["coordinates"]["coordinates"][1],
                'lng': tweet["tweet"]["geo"]["coordinates"]["coordinates"][0]
            }
            try:
                alert = message[:message.index(". Details")]
            except ValueError:
                alert = message

            if posted < 1:
                posted = "Reported in the past hour"
            else:
                posted = f"Reported {int(posted)} hours ago"

        return {"id": tweet["tweet"]["id"],
                "magnitude": magnitude, "coordinates": coordinates,
                "reported": posted + " - @earthquakeBot",
                "message": alert}
