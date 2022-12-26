from server.gateways.data.resources.providers.sports.sources.ESPN.interface import ESPNProvider


class SportsAggregator:

    espn = ESPNProvider()

    def __init__(self, provider=None):
        pass

    def get_leagues(self):
        sports_leagues = self.espn.get_sports_leagues()
        return sports_leagues

    def get_league(self, sport=None):
        league = self.espn.get_sports_leagues(sport=sport)
        return league

    def get_events(self, league=None, status=None):
        if status:
            status = status.lower()

        if status == "scheduled":
            scheduled_events = self.espn.get_espn_data(
                league=league, detail="schedule")
            return scheduled_events
        if status == "in_progress":
            in_progress_events = self.espn.get_espn_data(
                league=league, detail="in_progress")
            return in_progress_events
        if status == "completed":
            completed_events = self.espn.get_espn_data(
                league=league, detail="completed")
            return completed_events
        if status == "close":
            close_events = self.espn.get_espn_data(
                league=league, detail="close")
            return close_events

        if status == "scoreboard":
            scoreboard = self.espn.get_espn_data(
                league=league, detail="scoreboard")
            return scoreboard
