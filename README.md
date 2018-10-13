# MyZWave
Personal web API based on python-OpenZWave 

Tested with python 3.6 on Mac and Ubuntu, recommended to use `virtualenv`

## How to run

1. Install required packages via `pip install -r requirements.txt`
2. Run `python myzwave.py`

## API endpoints
* GET http://127.0.0.1:5000/switch/<node-no\>/on -> turn the related switch on
* GET http://127.0.0.1:5000/switch/<node-no\>/off -> turn the related switch off
* GET http://127.0.0.1:5000/switch/<node-no\>/toggle -> toggle the related switch (on -> off, off -> on)
* GET http://127.0.0.1:5000/switch/<node-no\>/status -> get status of switch
