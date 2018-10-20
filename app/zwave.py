import logging
import sys, os

from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time

class MyZwave:
    device="/dev/ttyACM0"
    config_path="/home/pi/Documents/Development/Python/python-openzwave-0.3.2/openzwave/config"
    log="Debug"
    network = None
    options = None

    def __init__(self):
        self.device="/dev/ttyACM0"
        self.config_path="/home/pi/Documents/Development/Python/python-openzwave-0.3.2/openzwave/config"
        self.log="Debug"
        self.network = None
        self.options = None

    def initZwave(self):
        self.options = ZWaveOption(self.device, config_path=self.config_path, user_path=".", cmd_line="")
        self.options.set_log_file("MyZWave_log.log")
        self.options.set_append_log_file(False)
        self.options.set_console_output(False)
        #self.options.set_console_output(True)
        self.options.set_save_log_level(self.log)
        self.options.set_logging(False)
        self.options.lock()

        self.network = ZWaveNetwork(self.options, log=None)

        time_started=0
        print("*** Waiting for network to awake: ")
        for i in range(0,300):
            if self.network.state >= self.network.STATE_AWAKED:
                print(" done")
                break
            else:
                sys.stdout.write(".")
                sys.stdout.flush()
                time_started += 1
                time.sleep(1.0)

        if self.network.state < self.network.STATE_AWAKED:
            print(".")
            print("Network is not awaked")
        for i in range(0,300):
            if self.network.state >= self.network.STATE_READY:
                print(" done in{} seconds".format(time_started))
                break
            else:
                sys.stdout.write(".")
                sys.stdout.flush()
                time_started += 1
                time.sleep(1.0)

        if not self.network.is_ready:
            print(".")
            print("Network is not ready")

    def toggleSwitch(self,nodeNum):
        node=self.network.nodes[nodeNum]
        print("Node: {}".format(node))
        val=node.get_switches().keys()[0]
        print("Values: {}".format(val))
        state = node.get_switch_state(val)
        print("State: {}".format(state))
        node.set_switch(val,not state)
        time.sleep(0.2)
        state = node.get_switch_state(val)
        return "on" if state else "off"

    def getSwitchStatus(self, nodeNum):
        node = self.network.nodes[nodeNum]
        val = node.get_switches().keys()[0]
        state = node.get_switch_state(val)
        return "on" if state else "off"

    def getInt(self, strNo):
        if strNo == None:
            return 0
        else:
            try:
                temp = int(strNo)
            except ValueError:
                temp = 0
            return temp
