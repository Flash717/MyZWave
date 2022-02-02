import app.zwave as zw
import logging
import app.scheduler as sched
from flask import Flask

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('openzwave')

app = Flask(__name__)

myzwave = zw.MyZwave()


@app.route('/')
def index():
    return "Hello World!"


@app.route('/switch/<nodeNo>/toggle')
def switchToggle(nodeNo=None):
    if nodeNo == None:
        return "No NodeNumber provided."
    myzwave.initZwave()
    status = myzwave.toggleSwitch(myzwave.getInt(nodeNo))
    myzwave.network.stop()
    return "Switched {}.".format(status)


@app.route('/switch/<nodeNo>/status')
def switchStatus(nodeNo=None):
    myzwave.initZwave()
    status = myzwave.getSwitchStatus(myzwave.getInt(nodeNo))
    myzwave.network.stop()
    return "Switch is {}.".format(status)


@app.route('/switch/<nodeNo>/on')
def switchOn(nodeNo=None):
    if nodeNo == None:
        return "No NodeNumber provided."
    myzwave.initZwave()
    status = myzwave.getSwitchStatus(myzwave.getInt(nodeNo))
    if status == "off":
        status = myzwave.toggleSwitch(myzwave.getInt(nodeNo))
    myzwave.network.stop()
    return "Switch is {}.".format(status)


@app.route('/switch/<nodeNo>/off')
def switchOff(nodeNo=None):
    if nodeNo == None:
        return "No node number provided."
    status = toggle_switch(nodeNo)
    return "Switch is {}".format(status)


def toggle_switch(nodeNo):
    myzwave.initZwave()
    status = myzwave.getSwitchStatus(myzwave.getInt(nodeNo))
    if status == "on":
        status = myzwave.toggleSwitch(myzwave.getInt(nodeNo))
    myzwave.network.stop()
    return status


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    sched = sched.Scheduler()
    sched.run_scheduler()
