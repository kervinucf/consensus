from server.gateways.data.resources.providers.weather.sources.PyWeather.helpers import get_weather


class PyWeatherProvider:

    def __init__(self):
        self.session_cache = {}

    def get_forecast(self, location):
        try:
            return self.session_cache[location]
        except KeyError:
            self.session_cache[location] = dict(get_weather(location))
            return self.session_cache[location]

    def get_extended_forecast(self, location):
        return self.get_forecast(location)['extended_forecast']

    def get_current_forecast(self, location):
        return self.get_forecast(location)['current_forecast']

    def get_sunrise(self, location):
        return self.get_current_forecast(location)['sunrise']

    def get_sunset(self, location):
        return self.get_current_forecast(location)['sunset']

    def get_sun_phases(self, location):
        return {
            "sunrise": self.get_current_forecast(location)['sunrise'],
            "sunset": self.get_current_forecast(location)['sunset']
        }

    def get_moonrise(self, location):
        return self.get_current_forecast(location)['moonrise']

    def get_moonset(self, location):
        return self.get_current_forecast(location)['moonset']

    def get_moon_phases(self, location):
        return {
            "moonrise": self.get_current_forecast(location)['moonrise'],
            "moonset": self.get_current_forecast(location)['moonset']
        }

