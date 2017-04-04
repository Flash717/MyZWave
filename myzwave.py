import logging
import sys, os
import resource
from flask import Flask
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('openzwave')

import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time

app = Flask(__name__)

device="/dev/ttyACM0"
config_path="/home/pi/Documents/Development/Python/python-openzwave-0.3.2/openzwave/config"
log="Debug"
network = None 

def initZwave():
	global network	
	options = ZWaveOption(device, config_path=config_path, user_path=".", cmd_line="")
	options.set_log_file("MyZWave_log.log")
	options.set_append_log_file(False)
	options.set_console_output(False)
	#options.set_console_output(True)
	options.set_save_log_level(log)
	options.set_logging(False)
	options.lock()

	network = ZWaveNetwork(options, log=None)

	time_started=0
	print("*** Waiting for network to awake: ")
	for i in range(0,300):
		if network.state >= network.STATE_AWAKED:
			print(" done")
			break
		else:
			sys.stdout.write(".")
			sys.stdout.flush()
			time_started += 1
			time.sleep(1.0)

	if network.state < network.STATE_AWAKED:
		print(".")
		print("Network is not awaked")
	for i in range(0,300):
		if network.state >= network.STATE_READY:
			print(" done in{} seconds".format(time_started))
			break
		else:
			sys.stdout.write(".")
			sys.stdout.flush()
			time_started += 1
			time.sleep(1.0)

	if not network.is_ready:
		print(".")
		print("Network is not ready")

def toggleSwitch(nodeNum):
	global network	
	node=network.nodes[nodeNum]
	print("Node: {}".format(node))
	val=node.get_switches().keys()[0]
	print("Values: {}".format(val))
	state = node.get_switch_state(val)
	print("State: {}".format(state))
	node.set_switch(val,not state)
	time.sleep(0.2)
	state = node.get_switch_state(val)
	return "on" if state else "off"

def getSwitchStatus(nodeNum):
	global network
	node = network.nodes[nodeNum]
	val = node.get_switches().keys()[0]
	state = node.get_switch_state(val)
	return "on" if state else "off"

def getInt(strNo):
	if strNo == None:
		return 0
	else:
		try:
			temp = int(strNo)
		except ValueError:
			temp = 0
		return temp

@app.route('/')
def index():
	return "Hello World!"

@app.route('/switch/<nodeNo>/toggle')
def switchToggle(nodeNo = None):
	if nodeNo == None:
		return "No NodeNumber provided."
	global network	
	initZwave()
	status = toggleSwitch(getInt(nodeNo))
	network.stop()
	return "Switched {}.".format(status)

@app.route('/switch/<nodeNo>/status')
def switchStatus(nodeNo = None):
	global network
	initZwave()
	status = getSwitchStatus(getInt(nodeNo))
	network.stop()
	return "Switch is {}.".format(status)

@app.route('/switch/<nodeNo>/on')
def switchOn(nodeNo = None):
	if nodeNo == None:
		return "No NodeNumber provided."
	global network
	initZwave()
	status = getSwitchStatus(getInt(nodeNo))
	if status == "off":
		status = toggleSwitch(getInt(nodeNo))
	network.stop()
	return "Switch is {}.".format(status)

@app.route('/switch/<nodeNo>/off')
def switchOff(nodeNo = None):
	if nodeNo == None:
		return "No node number provided."
	global network
	initZwave()
	status = getSwitchStatus(getInt(nodeNo))
	if status == "on":
		status = toggleSwitch(getInt(nodeNo))
	network.stop()
	return "Switch is {}".format(status)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
