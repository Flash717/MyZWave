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
        self._sleepnumber = 60
        self.nextstart = mktime(datetime.now().timetuple()) + (60 * 60 * 24)
        self.nextstop = mktime(datetime.now().timetuple()) - (60 * 60 * 24)
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
        """
        Schedule next weather check
        returns next sunrise and sunset timestamps
        """
        sunrise, sunset = weather.get_next_sun(self.lat, self.lon, self.apikey)
        logging.info('current time is {now}, next sunrise is {rise}, next sunset is {set}'.format(
            now = datetime.now(), rise = weather.d_of_t(sunrise), set = weather.d_of_t(sunset)))
        return sunrise, sunset

    def get_schedule(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rise=weather.d_of_t(self.nextstop).strftime("%Y-%m-%d %H:%M:%S")
        set=weather.d_of_t(self.nextstart).strftime("%Y-%m-%d %H:%M:%S")
        return {"current time": now, "next sunrise": rise, "next sunset": set}

    def run(self):
        """
        Running loop to check time and switch
        """
        log_counter = 0
        while self._running:
            if self.nextstart < mktime(datetime.now().timetuple()):
                logging.info('scheduled on for node {node}'.format(node=self.nodenumber))
                status = zw.switch_on(nodeNo=self.nodenumber)
                logging.info("scheduled switch is {}".format(status))
                self.nextstop, self.nextstart = self.schedule_weather()
            elif self.nextstop < mktime(datetime.now().timetuple()):
                logging.info('scheduled off for node {node}'.format(node=self.nodenumber))
                status = zw.switch_off(nodeNo=self.nodenumber)
                logging.info("scheduled switch is {}".format(status))
                self.nextstop, self.nextstart = self.schedule_weather()
            sleep(self._sleepnumber)
            log_counter += 1
            log_counter %= 15
            if (log_counter == 0):
                logging.info('check-in: {log}'.format(log = self.get_schedule()))

