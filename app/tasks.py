from celery import Celery

import app.zwave as zw

app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')

SWITCH_TOGGLE = 'toggle'
SWITCH_ON = 'on'
SWITCH_OFF = 'off'


@app.task
def run_toggle(node_no=3, switch=SWITCH_TOGGLE):
   	if node_no == None:
		return "No NodeNumber provided."
	zw.initZwave()
	status = zw.getSwitchStatus(zw.getInt(nodeNo))
    if (switch == SWITCH_TOGGLE) or (status == 'off' and switch == SWITCH_ON) or (status == 'on' and switch == SWITCH_OFF):
        status = zw.toggleSwitch(zw.getInt(node_no))
	zw.network.stop()
