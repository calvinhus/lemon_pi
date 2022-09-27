#!/usr/bin/python3

from locale import normalize
from DFRobot_ADS1115 import ADS1115
import os
import sys
import time
import board
import adafruit_dht
from flask import Flask, render_template, request

sys.path.append('../')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def getTemperature():

    # Print the values to the serial port
    #temperature = temp_sensor.temperature
    #humidity = temp_sensor.humidity
    temp_sensor = adafruit_dht.DHT11(board.D23)
    # return temperature, humidity
    try:
        # Print the values to the serial port
        temperature = temp_sensor.temperature
        humidity = temp_sensor.humidity
        if humidity is not None and temperature is not None:
            return temperature, humidity
        return 33, 77

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        # print(error.args[0])
        time.sleep(2.0)
    except Exception as error:
        temp_sensor.exit()
        raise error


def getSoilMoisture():
    soil_sensor = ADS1115()
    # set the IIC address
    soil_sensor.set_addr_ADS1115(0x48)
    # get the digital values from analog selected channel
    value = soil_sensor.read_voltage(0)
    return convertSoil(value['r'])


def convertSoil(data):
    # soil Moisture Sensor values are between 2700mV (Dry) and 1130mV (Wet) approximately
    normal = abs(data - 2700)/100
    # normalized values are between 0 and 16 approximately
    return (normal/16)*100


app = Flask(__name__)

# home route


@app.route('/')
def index():

    temperature, humidity = getTemperature()
    soil_moisture = getSoilMoisture()
    # variables to pass through to the web page
    templateData = {
        'humidity': round(humidity, 2),
        'temperature': round(temperature, 2),
        'soil_moisture': round(soil_moisture, 2)
    }
    # when a html request has been made return these values
    return render_template('index.html', **templateData)


if __name__ == '__main__':
    #app.jinja_env.cache = {}
    app.run(debug=True, host="0.0.0.0", port=5000)
