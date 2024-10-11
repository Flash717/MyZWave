import requests
from datetime import datetime
import time

url = 'http://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&APPID={apikey}'
default_sunrise_hour = 7
default_sunrise_minute = 15
default_sunset_hour = 18
default_sunset_minute = 30


def d_of_t(timestamp):
    """Helper function to convert timestamp to datetime
    :param timestamp: incoming timestamp
    :return datetime: converted datetime value
    """
    try:
        return datetime.fromtimestamp(timestamp)
    except (Exception):
        return timestamp

def get_next_sun(lat, lon, api_key):
    """Get next sunrise and sunset for provided latitude and longitude.

    :param lat: latitude float
    :param lon: longitude float
    :param api_key: api key for openweather API string
    :return sunrise, sunset: returns timestamp for next sunrise and sunset
    """
    response = requests.get(url.format(lat=lat, lon=lon, apikey=api_key))
    sunrise = int(time.mktime(datetime.now().replace(hour=default_sunrise_hour, minute=default_sunrise_minute).timetuple()))
    sunset = int(time.mktime(datetime.today().replace(hour=default_sunset_hour, minute=default_sunset_minute).timetuple()))
    if response.ok:
        body = response.json()
        sunrise = body['daily'][0]['sunrise']
        if d_of_t(sunrise) < datetime.now():
            sunrise = body['daily'][1]['sunrise']
        sunset = body['daily'][0]['sunset']
        if d_of_t(sunset) < datetime.now():
            sunset = body['daily'][1]['sunset']
    return sunrise, sunset
