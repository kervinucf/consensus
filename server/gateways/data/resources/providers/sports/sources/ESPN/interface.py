from server.gateways.data.resources.providers.sports.sources.ESPN.helpers import EspnAPI


class ESPNProvider:

    def __init__(self):
        pass

    @staticmethod
    def get_espn_data(league=None, detail=None):
        # make better !
        desc = detail.upper()

        espn_results = EspnAPI(league)
        if espn_results:
            if desc == "SCHEDULE":
                return espn_results.schedule
            elif desc == "IN_PROGRESS":
                return espn_results.in_progress
            elif desc == "COMPLETED":
                return espn_results.completed
            elif desc == "CLOSE":
                return espn_results.close
            elif desc == "SCOREBOARD":
                return espn_results.__dict__
        else:
            return None

    def get_sports_leagues(self, sport=None):
        if sport:
            return self.get_sports_leagues()[sport]

        return {
            "baseball": "mlb",
            "basketball": "nba",
            "football": "nfl",
            "soccer": ['usa.1', 'eng.1', 'eng.2', 'eng.3', 'eng.4', 'eng.5', 'esp.1', 'esp.2', 'ger.1', 'ger.2',
                       'fra.1',
                       'fra.2', 'tur.1', 'tur.2', 'ita.1', 'ita.2', 'fifa.world', 'uefa.champions']
        }
