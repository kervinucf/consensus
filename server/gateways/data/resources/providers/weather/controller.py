from server.gateways.data.resources.providers.weather.sources.PyWeather.interface import PyWeatherProvider
from server.gateways.data.resources.providers.weather.sources.EarthQuakeBot.interface import EarthQuakeBotProvider
from server.gateways.data.resources.providers.geo.sources.Nominatim.interface import NominatimProvider



class WeatherAggregator:

    py_weather = PyWeatherProvider()
    nominatim = NominatimProvider()
    earth_quake_bot = EarthQuakeBotProvider()

    def __init__(self, provider=None):
       pass

    def get_forecast(self, location, timeframe):

        if timeframe == "current":
            return self.py_weather.get_current_forecast(location=location)

        if timeframe == "extended":
            return self.py_weather.get_extended_forecast(location=location)

        if timeframe == "forecast":
            return self.py_weather.get_forecast(location=location)

    def get_sunrise(self, location):
        return self.py_weather.get_sunrise(location)

    def get_sunset(self, location):
        return self.py_weather.get_sunset(location)

    def get_sun_phases(self, location=None, timezone=None, sunrises=False, sunsets=False):

        if timezone:
            locations_in_timezone = self.nominatim.search_timezone_by_name(timezone)
            sun_phases = {}
            for timezone_location in locations_in_timezone:
                if sunrises:
                    sun_phases[timezone_location] = self.py_weather.get_sunrise(timezone_location)
                if sunsets:
                    sun_phases[timezone_location] = self.py_weather.get_sunset(timezone_location)
                else:
                    sun_phases[timezone_location] = {
                        "sunrise": self.py_weather.get_sunrise(timezone_location),
                        "sunset": self.py_weather.get_sunset(timezone_location)
                    }

            return sun_phases

        if location:
            if sunrises:
                return self.py_weather.get_sunrise(location)
            elif sunsets:
                return self.py_weather.get_sunset(location)

            else:
                return {
                    "sunrise": self.py_weather.get_sunrise(location),
                    "sunset": self.py_weather.get_sunset(location)
                }

    def get_moon_phases(self, location=None, timezone=None, moonrises=False, moonsets=False):

        if timezone:
            locations_in_timezone = self.nominatim.search_timezone_by_name(timezone)
            moon_phases = {}
            for timezone_location in locations_in_timezone:
                if moonrises:
                    moon_phases[timezone_location] = self.py_weather.get_moonrise(timezone_location)
                elif moonsets:
                    moon_phases[timezone_location] = self.py_weather.get_moonset(timezone_location)
                else:
                    moon_phases[timezone_location] = {
                        "moonrise": self.py_weather.get_moonrise(timezone_location),
                        "moonset": self.py_weather.get_moonset(timezone_location)
                    }

            return moon_phases

        if location:
            if moonrises:
                return self.py_weather.get_moonrise(location)
            elif moonsets:
                return self.py_weather.get_moonset(location)

            else:
                return {
                    "moonrise": self.py_weather.get_moonrise(location),
                    "moonset": self.py_weather.get_moonset(location)
                }

    def get_earthquakes(self):
        return self.earth_quake_bot.get_latest_earthquakes()
