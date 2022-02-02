# MyZWave
Personal web API based on python-OpenZWave using Flask

Tested with python 3.6 on Mac and Ubuntu, recommended to use `virtualenv`

## Prerequisites
Set following environment variables:  
- `OPENWEATHER_API_KEY`=\<your api key from openweathermap.org>  
- `LOCAL_LATITUDE`=\<your latitude>  
- `LOCAL_LONGITUDE`=\<your longitude>  
- `ZWAVE_NODE_NUMBER`=\<ZWave node to be controlled automatically> 

## How to run

1. Install required packages via `pip install -r requirements.txt`
2. Run `python myzwave.py`

## API endpoints
* GET http://127.0.0.1:5000/switch/<node-no\>/on -> turn the related switch on
* GET http://127.0.0.1:5000/switch/<node-no\>/off -> turn the related switch off
* GET http://127.0.0.1:5000/switch/<node-no\>/toggle -> toggle the related switch (on -> off, off -> on)
* GET http://127.0.0.1:5000/switch/<node-no\>/status -> get status of switch
