import app.zwave as zw
import logging
from flask import Flask

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger('openzwave')

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


@app.route('/switch/<nodeNo>/toggle')
def switchToggle(nodeNo=None):
    if nodeNo == None:
        return "No NodeNumber provided."
    zw.initZwave()
    status = zw.toggleSwitch(zw.getInt(nodeNo))
    zw.network.stop()
    return "Switched {}.".format(status)


@app.route('/switch/<nodeNo>/status')
def switchStatus(nodeNo=None):
    zw.initZwave()
    status = zw.getSwitchStatus(zw.getInt(nodeNo))
    zw.network.stop()
    return "Switch is {}.".format(status)


@app.route('/switch/<nodeNo>/on')
def switchOn(nodeNo=None):
    if nodeNo == None:
        return "No NodeNumber provided."
    zw.initZwave()
    status = zw.getSwitchStatus(zw.getInt(nodeNo))
    if status == "off":
        status = zw.toggleSwitch(zw.getInt(nodeNo))
    zw.network.stop()
    return "Switch is {}.".format(status)


@app.route('/switch/<nodeNo>/off')
def switchOff(nodeNo=None):
    if nodeNo == None:
        return "No node number provided."
    zw.initZwave()
    status = zw.getSwitchStatus(zw.getInt(nodeNo))
    if status == "on":
        status = zw.toggleSwitch(zw.getInt(nodeNo))
    zw.network.stop()
    return "Switch is {}".format(status)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    zw.initZwave()
