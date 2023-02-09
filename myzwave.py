import app.zwavehandler as zw
import logging
from threading import Thread
from app.scheduler import Scheduler
from flask import Flask

logging.basicConfig(level=logging.INFO, filename='myzwave.log', encoding='utf-8',
    format='%(asctime)s %(message)s')

logger = logging.getLogger('openzwave')

app = Flask(__name__)

sched = Scheduler()

@app.route('/')
def index():
    return "MyZWave"


@app.route('/switch/<node_no>/toggle')
def switch_toggle(node_no=None):
    if node_no == None:
        return "No NodeNumber provided."
    status = zw.toggle_switch(node_no)
    return "Switched {}.".format(status)


@app.route('/switch/<node_no>/status')
def switch_status(node_no=None):
    status = zw.get_status(node_no)
    return "Switch is {}.".format(status)


@app.route('/switch/<node_no>/on')
def switch_on(node_no=None):
    if node_no == None:
        return "No NodeNumber provided."
    status = zw.switch_on(node_no)
    return "Switch is {}.".format(status)


@app.route('/switch/<node_no>/off')
def switch_off(node_no=None):
    if node_no == None:
        return "No node number provided."
    status = zw.switch_off(node_no)
    return "Switch is {}".format(status)

@app.route('/schedule')
def get_schedule():
    return sched.get_schedule()

if __name__ == "__main__":
    try:
        t = Thread(target=sched.run, args=())
        t.start()
        app.run(host='0.0.0.0', debug=True)
    except Exception as e:
        logger.error('something went wrong ' + repr(e))
