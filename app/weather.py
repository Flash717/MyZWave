import requests
import os
import xml.etree.ElementTree as ET
from dateutil import parser

url = 'http://api.openweathermap.org/data/2.5/forecast?{type}={id}&APPID={apikey}&mode=xml'
api_key = os.environ['OPENWEATHER_API_KEY']


def get_sun(id, type='q'):
    response = requests.get(url.format(type=type, id=id, apikey=api_key))
    if response.ok:
        tree = ET.fromstring(response.content)
        sun = tree.find('sun')
        if sun is not None:
            return parser.parse(sun.attrib.get('rise')), parser.parse(sun.attrib.get('set'))
    return None, None
