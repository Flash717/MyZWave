from time import sleep, mktime
from datetime import datetime
import app.weather as weather
import zwavehandler as zw
import os
import sys

class Scheduler:

    def __init__(self):
        self.nextstop = 1
        self.nextstart = 1
        self._running = True
        self.lat = os.environ['LOCAL_LATITUDE']
        self.lon = os.environ['LOCAL_LONGITUDE']
        self.apikey = os.environ['OPENWEATHER_API_KEY']
        self.nodenumber = os.environ['ZWAVE_NODE_NUMBER']
        self.sleepnumber = 60

    def terminate(self):
        self._running = False

    def schedule_weather(self):
        """Schedule next weather check
        returns next sunrise and sunset timestamps
        """
        sunrise, sunset = weather.get_next_sun(self.lat, self.lon, self.apikey)
        print('next sunrise is {rise}, next sunset is {set}'.format(rise = sunrise, set = sunset))
        return sunrise, sunset

    def run(self):
        """Running loop to check time and switch
        """
        while self._running:
            if self.nextstart < mktime(datetime.now().timetuple()):
                zw.switch_on(nodeNo=self.nodenumber)
                self.nextstop, self.nextstart = self.schedule_weather()
            elif self.nextstop < mktime(datetime.now().timetuple()):
                zw.switch_off(nodeNo=self.nodenumber)
            sleep(self.sleepnumber)
            sys.stdout.write('.')

