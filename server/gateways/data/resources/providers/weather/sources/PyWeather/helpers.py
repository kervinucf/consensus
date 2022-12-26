import python_weather
import asyncio
from server.gateways.data.resources.providers.weather.sources.PyWeather.utils import LocationWeather
import requests

from logging import getLogger
from datetime import datetime
import datetime as dt

from tzwhere import tzwhere
import math


def get_weather(place):
    async def wttr_in(location):
        # declare the client. format defaults to the metric system (celcius, km/h, etc.)
        async with python_weather.Client(format=python_weather.IMPERIAL) as client:

            # fetch a weather forecast from a city
            wttr_data = await client.get(location)
            return vars(LocationWeather(wttr_data))

    return asyncio.run(wttr_in(place))


Country_Zones = ['America/New_York', 'Asia/Kolkata', 'Australia/Sydney',
                 'Canada/Atlantic', 'Brazil/East', 'Chile/EasterIsland', 'Cuba', 'Egypt',
                 'Europe/Amsterdam', 'Europe/Athens', 'Europe/Berlin', 'Europe/Istanbul',
                 'Europe/Jersey', 'Europe/London', 'Europe/Moscow', 'Europe/Paris',
                 'Europe/Rome', 'Hongkong', 'Iceland', 'Indian/Maldives', 'Iran',
                 'Israel', 'Japan', 'NZ', 'US/Alaska', 'US/Arizona', 'US/Central',
                 'US/East-Indiana']

logger = getLogger(__name__)


class Sun:

    def getSunriseTime(self, coords):
        return self.calcSunTime(coords, True)

    def getSunsetTime(self, coords):
        return self.calcSunTime(coords, False)

    def getCurrentUTC(self):
        now = datetime.now()
        return [now.day, now.month, now.year]

    def calcSunTime(self, coords, isRiseTime, zenith=90.8):

        # isRiseTime == False, returns sunsetTime

        day, month, year = self.getCurrentUTC()

        longitude = coords['lng']
        latitude = coords['lat']

        TO_RAD = math.pi / 180

        # 1. first calculate the day of the year
        N1 = math.floor(275 * month / 9)
        N2 = math.floor((month + 9) / 12)
        N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
        N = N1 - (N2 * N3) + day - 30

        # 2. convert the longitude to hour value and calculate an approximate time
        lngHour = longitude / 15

        if isRiseTime:
            t = N + ((6 - lngHour) / 24)
        else:  # sunset
            t = N + ((18 - lngHour) / 24)

        # 3. calculate the Sun's mean anomaly
        M = (0.9856 * t) - 3.289

        # 4. calculate the Sun's true longitude
        L = M + (1.916 * math.sin(TO_RAD * M)) + \
            (0.020 * math.sin(TO_RAD * 2 * M)) + 282.634
        L = self.forceRange(L, 360)  # NOTE: L adjusted into the range [0,360)

        # 5a. calculate the Sun's right ascension

        RA = (1 / TO_RAD) * math.atan(0.91764 * math.tan(TO_RAD * L))
        # NOTE: RA adjusted into the range [0,360)
        RA = self.forceRange(RA, 360)

        # 5b. right ascension value needs to be in the same quadrant as L
        Lquadrant = (math.floor(L / 90)) * 90
        RAquadrant = (math.floor(RA / 90)) * 90
        RA = RA + (Lquadrant - RAquadrant)

        # 5c. right ascension value needs to be converted into hours
        RA = RA / 15

        # 6. calculate the Sun's declination
        sinDec = 0.39782 * math.sin(TO_RAD * L)
        cosDec = math.cos(math.asin(sinDec))

        # 7a. calculate the Sun's local hour angle
        cosH = (math.cos(TO_RAD * zenith) - (sinDec * math.sin(TO_RAD * latitude))) / (
            cosDec * math.cos(TO_RAD * latitude))

        if cosH > 1:
            return {'status': False, 'msg': 'the sun never rises on this geo (on the specified date)'}

        if cosH < -1:
            return {'status': False, 'msg': 'the sun never sets on this geo (on the specified date)'}

        # 7b. finish calculating H and convert into hours

        if isRiseTime:
            H = 360 - (1 / TO_RAD) * math.acos(cosH)
        else:  # setting
            H = (1 / TO_RAD) * math.acos(cosH)

        H = H / 15

        # 8. calculate local mean time of rising/setting
        T = H + RA - (0.06571 * t) - 6.622

        # 9. adjust back to UTC
        UT = T - lngHour
        UT = self.forceRange(UT, 24)  # UTC time in decimal format (e.g. 23.23)

        # 10. Return
        hr = self.forceRange(int(UT), 24)
        min = round((UT - int(UT)) * 60, 0)

        return {
            'status': True,
            'decimal': UT,
            'hr': hr,
            'min': min
        }

    def forceRange(self, v, max):
        # force v to be >= 0 and < max
        if v < 0:
            return v + max
        elif v >= max:
            return v - max

        return v


def find_timezone(lat, lng):
    tz = tzwhere.tzwhere()
    return tz.tzNameAt(lat, lng)


def get_timezone(lat, lng, name=None):
    # find in db
    # if not in db, find in gateways
    timezone = None
    if name and not lat and not lng:
        location = name.upper()

        coordinates = find_coordinates(location)
        timezone = get_from_db(
            db=LocationDatabase,
            table='TimeZones',
            column=coordinates)

    if not timezone:
        timezone = get_from_db(
            db=LocationDatabase,
            table='TimeZones',
            column={'lat': lat, 'lng': lng})

    if not timezone:
        logger.debug('{} timezone not found in db'.format(name))
        timezone = find_timezone(lat=lat, lng=lng)
        if timezone:
            logger.debug('timezone found in gateways')
            update_record(db=LocationDatabase, table='TimeZones',
                          column={'lat': lat, 'lng': lng}, data=timezone)

    return timezone


def get_timezone_datetime(timezone):
    data = requests.get(
        'http://worldtimeapi.org/api/timezone/{}'.format(timezone)).json()

    try:
        return {
            "datetime": data['datetime'],
            "unixtime": data['unixtime'],
            "utc_datatime": data['utc_datetime'],

        }

    except KeyError:
        return None


def get_local_time(lat, lng):
    timezone = get_timezone(lat, lng)
    local_time = get_from_db(
        db=LocationDatabase,
        table='TimeZone Time',
        column=timezone)

    if not local_time:
        local_time = get_timezone_datetime(timezone)
        if local_time:
            update_record(db=LocationDatabase, table='TimeZone Time',
                          column=timezone, data=local_time)

    return local_time


def get_sunrise_sunset(coordinates, ignoreOffset=False):
    location_sun_monitor = Sun()

    behind = False
    sunset = location_sun_monitor.getSunsetTime(coordinates)
    sunrise = location_sun_monitor.getSunriseTime(coordinates)

    time_of_day = None

    try:
        hour_offset = int(sunset["hr"]) - 4
        if hour_offset < 0:
            hour_offset = 24 + hour_offset
            behind = True

        sunset = "{}:{}:{}".format(hour_offset, int(
            sunset["min"]), int(sunset["decimal"]))
    except KeyError:
        if sunset['msg'] == 'the sun never rises on this geo (on the specified date)':
            return {
                "sunrise_est": None,
                "sunset_est": None,
                "local_sunrise": None,
                "local_sunset": None,
                "offset": None,
                "time_of_day": "special-night",
                "behind_server_time": None
            }

    try:
        hour_offset = int(sunrise["hr"]) - 4
        if hour_offset < 0:
            hour_offset = 24 + hour_offset
            behind = True

        sunrise = "{}:{}:{}".format(hour_offset, int(sunrise["min"]),
                                    int(sunrise["decimal"]))
    except KeyError:
        if sunrise['msg'] == 'the sun never sets on this geo (on the specified date)':
            return {
                "sunrise_est": None,
                "sunset_est": None,
                "local_sunrise": None,
                "local_sunset": None,
                "offset": None,
                "time_of_day": "special-day",
                "behind_server_time": None
            }
    if ignoreOffset:
        offset = None
        local_time = datetime.now()
        local_time = local_time.strftime("%H:%M:%S")
        local_sunrise = sunrise
        local_sunset = sunset

    else:
        if sunset:
            server_sunset = get_sunrise_sunset({'lat': 40.7127281, 'lng': -74.0060152}, ignoreOffset=True)[
                "local_sunset"]
            time_difference = datetime.strptime(sunset,
                                                "%H:%M:%S") - datetime.strptime(server_sunset,
                                                                                "%H:%M:%S")

        if sunrise:
            server_sunrise = get_sunrise_sunset({'lat': 40.7127281, 'lng': -74.0060152}, ignoreOffset=True)[
                "local_sunrise"]
            time_difference = datetime.strptime(sunrise,
                                                "%H:%M:%S") - datetime.strptime(server_sunrise,
                                                                                "%H:%M:%S")

        if behind:
            time_difference = dt.timedelta(hours=24) - time_difference
            offset = (time_difference.seconds / 3600) - 24
        else:
            offset = 24 - time_difference.seconds / 3600

        if offset > 18:
            offset = offset - 24
        if offset < -6:
            offset = offset + 24

        local_time = dt.timedelta(hours=offset) + datetime.now()
        local_time = local_time.strftime("%H:%M:%S")

        # if local time between 2:00 and 6:00 am local time equal to dawn
        # if local time between 6:00 and 8:00 am local time equal to sunrise
        # if local time between 8:00 and 6:00 pm local time equal to day
        # if local time between 6:00 and 8:00 pm local time equal to sunset
        # if local time between 8:00 and 2:00 am local time equal to night
        local_sunrise = dt.timedelta(
            hours=offset) + datetime.strptime(sunrise, "%H:%M:%S")
        local_sunset = dt.timedelta(
            hours=offset) + datetime.strptime(sunset, "%H:%M:%S")

        if "02:00:00" <= local_time < "06:00:00":
            time_of_day = "dawn"
        elif "06:00:00" <= local_time < "08:00:00":
            time_difference = local_sunrise - datetime.strptime(local_time,
                                                                "%H:%M:%S")
            time_diff_hours = abs((time_difference.seconds / 3600) - 24)

            if time_diff_hours < 1.5:
                time_of_day = "sunrise"
            else:
                time_of_day = "morning"
        elif "08:00:00" <= local_time < "18:00:00":
            time_of_day = "day"
        elif "18:00:00" <= local_time < "20:00:00":

            time_difference = local_sunset - datetime.strptime(local_time,
                                                               "%H:%M:%S")
            time_diff_hours = abs((time_difference.seconds / 3600) - 24)

            if time_diff_hours < 1.25:
                time_of_day = "sunset"
            else:
                time_of_day = "evening"
        elif local_time >= "20:00:00" or local_time < "02:00:00":
            time_of_day = "night"

        local_sunrise = local_sunrise.strftime("%H:%M:%S")
        local_sunset = local_sunset.strftime("%H:%M:%S")

    return {
        "sunrise_est": sunrise,
        "sunset_est": sunset,
        "local_sunrise": local_sunrise,
        "local_sunset": local_sunset,
        "offset": offset,
        "time_of_day": time_of_day,
        "behind_server_time": behind
    }
