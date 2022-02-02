import zwave as zw

myzwave = zw.MyZwave()

def toggle_switch(nodeNo):
    myzwave.initZwave()
    status = myzwave.getSwitchStatus(myzwave.getInt(nodeNo))
    if status == "on":
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
