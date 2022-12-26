from datetime import datetime, timedelta
from server.gateways.data.resources.providers.geo.sources.Nominatim.utils\
    import get_coordinates
from dateutil import parser
from dataclasses import dataclass


def get_current_time(future=None, date=False):

    if date:
        return datetime.now().date()
    if future:
        return get_current_time() + timedelta(seconds=future).total_seconds()
    return datetime.utcnow().timestamp()


def get_time_since(created):
    then = parser.parse(created).replace(
        tzinfo=None)  # Random date in the past
    return get_current_time() - then.timestamp()


@dataclass
class SportsEvent:

    def __init__(self, league, event_data):
        # score
        # teams - abb, pic, record, home, away
        # venue - name, geo, attendance
        self.league = league

        self.id = event_data['id']
        self.uid = event_data['uid']
        self.date = event_data['date']
        self.home_team = None
        self.away_team = None
        self.close_game = None

        self.season = event_data['season']

        self.state = event_data['status']["type"]["name"]
        self.period = event_data['status']["period"]
        score1 = None

        for competitor in event_data["competitions"][0]["competitors"]:
            league_1 = ["NBA", "NCAAF", "NFL"]
            league_2 = ["MLB"]
            if self.state == "STATUS_IN_PROGRESS":
                if score1 is None:
                    score1 = competitor["score"]
                else:
                    if self.league in league_2:
                        max_periods = 9
                    elif self.league in league_1:
                        max_periods = 4
                    if self.period / max_periods > 0.75:
                        if self.league in league_2 and abs(int(competitor["score"]) - int(score1)) < 2:
                            self.close_game = True
                        elif self.league in league_1 and abs(int(competitor["score"]) - int(score1)) < 8:
                            self.close_game = True
                    else:
                        self.close_game = False

            try:
                records = competitor["records"][0]["summary"]
            except KeyError:
                records = None
            try:
                logo = competitor["team"]["logo"]
            except KeyError:
                logo = None

            try:
                altColor = competitor["team"]["alternateColor"]
            except KeyError:
                altColor = None

            try:
                color = competitor["team"]["color"]
            except KeyError:
                color = None

            try:
                score = competitor["score"]
            except KeyError:
                score = None

            try:
                name = competitor["team"]["displayName"]
            except KeyError:
                name = None

            try:
                abbreviation = competitor["team"]["abbreviation"]
            except KeyError:
                abbreviation = None

            info = {
                "name": name,
                "abbreviation": abbreviation,
                "logo": logo,
                "altColor": altColor,
                "color": color,
                "score": score,
                "record": records
            }
            if competitor["homeAway"] == "home":
                self.home_team = info
            else:
                self.away_team = info

        self.attendance = event_data["competitions"][0]['attendance']
        self.venue = event_data["competitions"][0]['venue']
        self.venue["coordinates"] = get_coordinates(
            f"{self.venue['fullName']}")


@dataclass
class League:

    def __init__(self, response):
        res_data = response["res"]
        if self.in_season(season=res_data["leagues"][0]['season']):
            # ##############################################################
            self.today = []
            self.upcoming = []
            self.schedule = []
            self.in_progress = []
            self.completed = []
            self.close = []
            # ##############################################################
            self.name = res_data['leagues'][0]["name"]
            self.abbreviation = res_data["leagues"][0]['abbreviation']
            try:
                self.season = res_data['season']['types']
            except KeyError:
                self.season = None
            try:
                self.week = res_data['week']['number']
            except KeyError:
                self.week = None
            self.events = self.process_events(events=res_data['events'])

    def in_season(self, season):
        start = season['startDate']
        end = season['endDate']

        today = str(get_current_time(date=True))

        if end >= today >= start:
            return True

    def process_events(self, events):
        events_found = {}
        for event in events:
            game = SportsEvent(league=self.abbreviation,
                               event_data=event).__dict__

            events_found[event['id']] = game
            hours_until = get_time_since(game['date']) / 60 / 60
            if hours_until > -24:
                self.today.append(game['id'])
            elif hours_until < -24:
                self.upcoming.append(game['id'])
            if game['state'] == "STATUS_IN_PROGRESS":
                self.in_progress.append(game['id'])
            elif game['state'] == "STATUS_FINAL":
                self.completed.append(game['id'])
            elif game["close_game"]:
                self.close.append(game["id"])
            self.schedule.append(game['id'])
        return events_found

# dict_keys(['id', 'uid', 'date', 'name', 'shortName', 'season', 'competitions', 'links', 'earth', 'status'])
