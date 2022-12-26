from server.gateways.data.resources.providers.twtr.sources.Twitter.api.resolver import TwitterQuery


class TrendsProvider:

    @staticmethod
    def search_trends_in(location=None):

        location = location.upper()

        api_trends = TwitterQuery(latest_trends_in=location)
        if api_trends:

            try:
                return api_trends.__dict__
            except AttributeError:
                print(f"AttributeError {api_trends}")
                return None
        else:
            return None

    def global_trends(self):
        return {
            'na': {
                'usa': self.search_trends_in('United States'),
                'can': self.search_trends_in('Canada'),
                'mex': self.search_trends_in('Mexico')
            },
            'sa': {
                'br': self.search_trends_in('Brazil'),
                'vz': self.search_trends_in('Venezuela'),
                'pu': self.search_trends_in('Peru'),
                'co': self.search_trends_in('Colombia'),
                'ag': self.search_trends_in('Argentina')
            },
            'as': {
                'vt': self.search_trends_in('Vietnam'),
                'io': self.search_trends_in('Indonesia'),
                'in': self.search_trends_in('India'),
                'sa': self.search_trends_in('Saudi Arabia'),
            },
            'eu': {
                'ua': self.search_trends_in('Ukraine'),
                'it': self.search_trends_in('Italy'),
                'sp': self.search_trends_in('Spain'),
                'gu': self.search_trends_in('Germany'),
                'fr': self.search_trends_in('France'),
                'uk': self.search_trends_in('United Kingdom'),
                'ru': self.search_trends_in('Russia')
            },
            'af': {
                'sa': self.search_trends_in('South Africa'),
                'eg': self.search_trends_in('Egypt'),
                'jo': self.search_trends_in('Johannesburg'),
                'ni': self.search_trends_in('Nigeria')
            },
        }
