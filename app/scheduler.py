import threading
from time import sleep, mktime
from datetime import datetime
import app.weather as weather
import zwavehandler as zw
import os

class Scheduler:
    lat = os.environ['LOCAL_LATITUDE']
    lon = os.environ['LOCAL_LONGITUDE']
    apikey = os.environ['OPENWEATHER_API_KEY']
    nodenumber = os.environ['ZWAVE_NODE_NUMBER']
    sleepnumber = 60

    nextstart = None
    nextstop = None

    def __init__(self):
        self.nextstop = 1
        self.nextstart = 1

    def schedule_weather(self):
        """Schedule next weather check
        returns next sunrise and sunset timestamps
        """
        sunrise, sunset = weather.get_next_sun(self.lat, self.lon, self.apikey)
        print('next sunrise is {rise}, next sunset is {set}'.format(rise = sunrise, set = sunset))
        return sunrise, sunset

    def check_run(self, nodenumber):
        """Running loop to check time and switch
        """
        while True:
            if self.nextstart < mktime(datetime.now().timetuple()):
                zw.switchOn(nodeNo=nodenumber)
                self.nextstop, self.nextstart = self.schedule_weather()
            elif self.nextstop < mktime(datetime.now().timetuple()):
                zw.switchOff(nodeNo=nodenumber)
            sleep(self.sleepnumber)
            print('.')

    def run_scheduler(self):
        """
        Runs thread for regular checking on switch status
        """
        try:
            print('starting scheduler for node ' + self.nodenumber)
            t1 = threading.Thread(target=self.check_run, args=(self.nodenumber,))
            t1.start()
            print('scheduler started')
        except Exception as e:
            print('something went wrong ' + repr(e))
