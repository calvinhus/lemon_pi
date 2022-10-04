#!/usr/bin/env python

import os
import sys
import time
import RPi.GPIO as GPIO
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# GPIO setup
relay_pin = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

# Create sensor object
from DFRobot_ADS1115 import ADS1115
ads1115 = ADS1115()


def soil_moisture(sensor):
    # Set the IIC address
    sensor.set_addr_ADS1115(0x49)
    # Get the Digital Value from selected channel
    adc0 = sensor.read_voltage(0)
    value = adc0['r']
    # values are between 2700mV (Dry) and 1130mV (Wet) approximately
    normal = abs(value - 2700)/100
    # normalized values are between 0 and 16 approximately
    percnt = round((normal/16)*100, 2)

    return percnt

def water(pin, level):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if level < 15:
#        GPIO.output(pin, GPIO.HIGH)
#        time.sleep(2)
#        GPIO.output(pin, GPIO.LOW)
        print(f"{now} - Lemon tree watered! Soil moisture was at {level}%")
    else:
        print(f"{now} - No watering needed. Soil moisture is at {level}%")

# Check soil moisture level
soil_level = soil_moisture(ads1115)

# Check if it needs watering
water(relay_pin, soil_level)

GPIO.cleanup()
