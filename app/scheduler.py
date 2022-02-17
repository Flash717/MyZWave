from time import sleep, mktime
from datetime import datetime
import app.weather as weather
import zwavehandler as zw
import os
import sys
from dotenv import load_dotenv

class Scheduler:

    def __init__(self):
        self._running = True
        self.sleepnumber = 60
        self.nextstart = mktime(datetime.now().timetuple()) + 1
        self.nextstop = mktime(datetime.now().timetuple()) -1
        self._load_env_vars()
        if self._running:
            self.nextstop, self.nextstart = self.schedule_weather()

    def terminate(self):
        self._running = False

    def _load_env_vars(self):
        try:
            load_dotenv()
            self.lat = os.environ['LOCAL_LATITUDE']
            self.lon = os.environ['LOCAL_LONGITUDE']
            self.apikey = os.environ['OPENWEATHER_API_KEY']
            self.nodenumber = os.environ['ZWAVE_NODE_NUMBER']
        except Exception as e:
            print("could not load environment vars: " + repr(e))
            self._running = False

    def schedule_weather(self):
        """Schedule next weather check
        returns next sunrise and sunset timestamps
        """
        sunrise, sunset = weather.get_next_sun(self.lat, self.lon, self.apikey)
        print('current time is {now}, next sunrise is {rise}, next sunset is {set}'.format(
            now = datetime.now(), rise = weather.d_of_t(sunrise), set = weather.d_of_t(sunset)))
        return sunrise, sunset

    def run(self):
        """Running loop to check time and switch
        """
        while self._running:
            if self.nextstart < mktime(datetime.now().timetuple()):
                print('scheduled on')
                zw.switch_on(nodeNo=self.nodenumber)
                self.nextstop, self.nextstart = self.schedule_weather()
            elif self.nextstop < mktime(datetime.now().timetuple()):
                print('scheduled off')
                zw.switch_off(nodeNo=self.nodenumber)
            sleep(self.sleepnumber)
            sys.stdout.write('x')

