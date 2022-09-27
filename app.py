#!/usr/bin/python3

from locale import normalize
from DFRobot_ADS1115 import ADS1115
import os
import sys
import time
from flask import Flask, render_template, request

sys.path.append('../')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

soil_sensor = ADS1115()


def convertSoil(data):
    # soil Moisture Sensor values are between 2700mV (Dry) and 1130mV (Wet) approximately
    normal = abs(data - 2700)/100
    # normalized values are between 0 and 16 approximately
    return (normal/16)*100


app = Flask(__name__)

# home route


@app.route('/')
def index():

    # set the IIC address
    soil_sensor.set_addr_ADS1115(0x48)
    # get the digital values from analog selected channel
    value = soil_sensor.read_voltage(0)
    soil_moisture = convertSoil(value['r'])

    # variables to pass through to the web page
    templateData = {
        'title': 'Smart Garden',
        'humidity': 75,
        'temperature': 35,
        'light': 125,
        'soil_moisture': round(soil_moisture,2)
    }
    # when a html request has been made return these values
    return render_template('index.html', **templateData)


if __name__ == '__main__':
    #app.jinja_env.cache = {}
    app.run(debug=True, host="0.0.0.0", port=5000)
