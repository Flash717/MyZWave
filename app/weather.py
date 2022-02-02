import requests
import os
from datetime import datetime

url = 'http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&APPID={apikey}'
api_key = os.environ['OPENWEATHER_API_KEY']

def d_of_t(timestamp):
    """Helper function to convert timestamp to datetime
    :param timestamp: incoming timestamp
    :return datetime: converted datetime value
    """
    try:
        return datetime.fromtimestamp(timestamp)
    except (Exception):
        return timestamp

def get_next_sun(lat, lon):
    """Get next sunrise and sunset for provided latitude and longitude.

    :param lat: latitude float
    :param lon: longitude float
    :return sunrise, sunset: returns timestamp for next sunrise and sunset
    """
    response = requests.get(url.format(lat=lat, lon=lon, apikey=api_key))
    if response.ok:
        body = response.json()
        sunrise = body['daily'][0]['sunrise']
        if d_of_t(sunrise) < datetime.now():
            sunrise = body['daily'][1]['sunrise']
        sunset = body['daily'][0]['sunset']
        if d_of_t(sunset) < datetime.now():
            sunset = body['daily'][1]['sunset']
        return sunrise, sunset
    return None, None

if __name__ == '__main__':
    sunrise, sunset = get_next_sun(32.18,-96.81)
    print(d_of_t(sunrise))
    print(d_of_t(sunset))
