from time import sleep, mktime
from datetime import datetime
import app.weather as weather
import zwavehandler as zw
import os
import sys
import logging
# from dotenv import load_dotenv

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
            # load_dotenv()
            self.lat = os.environ.get('LOCAL_LATITUDE', 0)
            self.lon = os.environ.get('LOCAL_LONGITUDE', 0)
            self.apikey = os.environ.get('OPENWEATHER_API_KEY', 'n/a')
            self.nodenumber = os.environ.get('ZWAVE_NODE_NUMBER', 1)
        except Exception as e:
            logging.error("could not load environment vars: " + repr(e))
            self._running = False

    def schedule_weather(self):
        """Schedule next weather check
        returns next sunrise and sunset timestamps
        """
        sunrise, sunset = weather.get_next_sun(self.lat, self.lon, self.apikey)
        logging.info('current time is {now}, next sunrise is {rise}, next sunset is {set}'.format(
            now = datetime.now(), rise = weather.d_of_t(sunrise), set = weather.d_of_t(sunset)))
        return sunrise, sunset

    def run(self):
        """Running loop to check time and switch
        """
        while self._running:
            if self.nextstart < mktime(datetime.now().timetuple()):
                logging.info('scheduled on')
                zw.switch_on(nodeNo=self.nodenumber)
                self.nextstop, self.nextstart = self.schedule_weather()
            elif self.nextstop < mktime(datetime.now().timetuple()):
                logging.info('scheduled off')
                zw.switch_off(nodeNo=self.nodenumber)
            sleep(self.sleepnumber)
            logging.info('check-in: next sunrise is {rise}, next sunset is {set}'.format(
                rise=weather.d_of_t(self.nextstop), set=weather.d_of_t(self.nextstart)))

