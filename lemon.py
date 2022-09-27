#!/usr/bin/python3

from DFRobot_ADS1115 import ADS1115
import os
import sys
import time
from flask import Flask, render_template, request

sys.path.append('../')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

soil_sensor = ADS1115()

app = Flask(__name__)


# home route
@app.route('/')
def index():

    # Set the IIC address
    soil_sensor.set_addr_ADS1115(0x48)
    # Get the Digital Value of Analog of selected channel
    soil_moisture = soil_sensor.read_voltage(0)

    # variables to pass through to the web page
    templateData = {
        'title': 'Smart Garden',
        'humidity': 75,
        'temperature': 35,
        'light': 125,
        'temp': soil_moisture
    }
    # when a html request has been made return these values
    return render_template('index.html', **templateData)


if __name__ == '__main__':
    #app.jinja_env.cache = {}
    app.run(debug=True, host="0.0.0.0", port=5000)
