from multiprocessing import Process
import app.zwavehandler as zw
import logging
import json
from app.scheduler import Scheduler
from flask import Flask

logging.basicConfig(level=logging.DEBUG, filename='myzwave.log', encoding='utf-8',
    format='%(asctime)s - %(name)s - %(message)s')

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

@app.route('/nodeinfo')
def get_node_info():
    result = {}
    nodes = zw.get_nodes()
    logger.debug("got node information")
    logger.debug("length: " + str(len(nodes)) + "\ttype: " + str(type(nodes)))
    for i in nodes:
        try:
            node = nodes[i]
	    logger.debug(node)
            switches = node.get_switches()
            logger.debug(str(i) + ": switches: " + str(switches) + "\tlength: " + str(len(switches)))
            result[i] = {'switches': str(switches)}
        except Exception as e:
            logger.error(str(node) + " == " + str(e))
    logger.debug(result)
    return json.dumps(result)

if __name__ == "__main__":
    try:
        p = Process(target=sched.run, name='MyZWave-Scheduler' ,args=())
        p.start()
        app.run(host='0.0.0.0', debug=True)
    except Exception as e:
        logger.error('something went wrong ' + repr(e))
