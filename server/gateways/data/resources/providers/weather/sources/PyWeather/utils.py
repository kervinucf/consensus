from dataclasses import dataclass


@dataclass
class Forecast:
    day = {}

    def __init__(self, forecast):
        try:
            self.sunrise = forecast.astronomy.sun_rise.strftime("%H:%M")
        except AttributeError:
            self.sunrise = None

        try:
            self.sunset = forecast.astronomy.sun_set.strftime("%H:%M")
        except AttributeError:
            self.sunset = None

        try:
            self.moonrise = forecast.astronomy.moon_rise.strftime("%H:%M")
        except AttributeError:
            self.moonrise = None

        try:
            self.moonset = forecast.astronomy.moon_set.strftime("%H:%M")
        except AttributeError:
            self.moonset = None

        self.temperature = forecast.temperature
        self.high_temp = forecast.highest_temperature
        self.low_temp = forecast.lowest_temperature


@dataclass
class LocationWeather:

    def __init__(self, weather):
        self.extended_forecast = self.create_extended_forecast(weather)
        self.current_forecast = self.extended_forecast[0]
        # ###############################################
        self.coordinates = weather.location

    @staticmethod
    def create_hourly_forecast(hourly):
        hourly_forecast = {
            "chance_of_rain": hourly.chance_of_rain,
            "chance_of_snow": hourly.chance_of_snow,
            "chance_of_sunshine": hourly.chance_of_sunshine,
            "description": hourly.description,
            "feels_like": hourly.feels_like,
            "temperature": hourly.temperature
        }
        return hourly_forecast

    def create_extended_forecast(self, weather):
        week_forecast = {}
        plus_day = 0
        for forecast in weather.forecasts:
            DayForecast = Forecast(forecast)
            for hourly in forecast.hourly:
                DayForecast.day = self.create_hourly_forecast(hourly)

            week_forecast[plus_day] = DayForecast.__dict__
            plus_day += 1
        return week_forecast
