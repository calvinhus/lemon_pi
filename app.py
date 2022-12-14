#!/usr/bin/python3
from DFRobot_ADS1115 import ADS1115
import os
import sys
import time
from datetime import datetime
import board
import adafruit_dht
from picamera import PiCamera
from flask import Flask, render_template, send_file

sys.path.append('../')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def getTemperature():
    temp_sensor = adafruit_dht.DHT11(board.D23)
    temperature = temp_sensor.temperature
    humidity = temp_sensor.humidity

    return temperature, humidity


def getSoilMoisture():
    soil_sensor = ADS1115()
    # set the IIC address
    soil_sensor.set_addr_ADS1115(0x49)
    # get the digital values from analog selected channel
    value = soil_sensor.read_voltage(0)
    return convertSoil(value['r'])


def convertSoil(data):
    # soil Moisture Sensor values are between 2700mV (Dry) and 1130mV (Wet) approximately
    normal = abs(data - 2700)/100
    # normalized values are between 0 and 16 approximately
    return (normal/16)*100


app = Flask(__name__)


@app.route('/')
def index():

    # temperature, humidity = getTemperature()
    soil_moisture = getSoilMoisture()
    # variables to pass through to the web page
    templateData = {
        'humidity': 50,  # round(humidity, 2),
        'temperature': 25,  # round(temperature, 2),
        'soil_moisture': round(soil_moisture, 2)
    }
    # when a html request has been made return these values
    return render_template('index.html', **templateData)


@app.route('/picture')
def get_picture():
    # clean up old pictures
    os.system('sudo rm /home/pi/lemon_pi/static/images/*.jpg')
    # create Camera object
    camera = PiCamera()
    # set name of picture: path + timestamp
    path = "/home/pi/lemon_pi/static/images/"
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mm")
    full_path = path + timestamp + ".jpg"
    # take picture and close camera object
    camera.capture(full_path)
    camera.close()

    return send_file(full_path)


if __name__ == '__main__':
    #app.jinja_env.cache = {}
    app.run(debug=True, host="0.0.0.0", port=5000)
