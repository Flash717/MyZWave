import app.zwavehandler as zw
import logging
from threading import Thread
from app.scheduler import Scheduler
from flask import Flask

logging.basicConfig(level=logging.INFO, filename='myzwave.log', encoding='utf-8',
    format='%(asctime)s %(message)s')

logger = logging.getLogger('openzwave')

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"


@app.route('/switch/<nodeNo>/toggle')
def switchToggle(nodeNo=None):
    if nodeNo == None:
        return "No NodeNumber provided."
    status = zw.toggle_switch(nodeNo)
    return "Switched {}.".format(status)


@app.route('/switch/<nodeNo>/status')
def switchStatus(nodeNo=None):
    status = zw.get_status(nodeNo)
    return "Switch is {}.".format(status)


@app.route('/switch/<nodeNo>/on')
def switchOn(nodeNo=None):
    if nodeNo == None:
        return "No NodeNumber provided."
    status = zw.switch_on(nodeNo)
    return "Switch is {}.".format(status)


@app.route('/switch/<nodeNo>/off')
def switchOff(nodeNo=None):
    if nodeNo == None:
        return "No node number provided."
    status = zw.switch_off(nodeNo)
    return "Switch is {}".format(status)

if __name__ == "__main__":
    try:
        sched = Scheduler()
        t = Thread(target=sched.run, args=())
        t.start()
        app.run(host='0.0.0.0', debug=True)
        sched.terminate()
        t.join()
    except Exception as e:
        logger.error('something went wrong ' + repr(e))
