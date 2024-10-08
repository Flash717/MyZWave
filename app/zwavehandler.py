import zwave as zw
import logging

myzwave = zw.MyZwave()
logger = logging.getLogger('myZwave')

def toggle_switch(nodeNo):
    myzwave.initZwave()
    status = myzwave.toggleSwitch(myzwave.getInt(nodeNo))
    myzwave.network.stop()
    return status

def switch_on(nodeNo):
    myzwave.initZwave()
    status = myzwave.getSwitchStatus(myzwave.getInt(nodeNo))
    if status == "off":
        status = myzwave.toggleSwitch(myzwave.getInt(nodeNo))
    myzwave.network.stop()
    return status

def switch_off(nodeNo):
    myzwave.initZwave()
    status = myzwave.getSwitchStatus(myzwave.getInt(nodeNo))
    if status == "on":
        status = myzwave.toggleSwitch(myzwave.getInt(nodeNo))
    myzwave.network.stop()
    return status

def get_status(nodeNo):
    myzwave.initZwave()
    status = myzwave.getSwitchStatus(myzwave.getInt(nodeNo))
    myzwave.network.stop()
    return status

def get_nodes():
    myzwave.initZwave()
    logger.debug("ZWave initialized")
    result = myzwave.getNodes()
    logger.debug("Node information received")
    myzwave.network.stop()
    return result
