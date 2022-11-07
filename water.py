#!/usr/bin/env python

# import libraries
import time
import RPi.GPIO as GPIO
import time
from scripts.soil_moisture_sensor import SoilMoistureLevel
from scripts.mail import SendMail
from datetime import datetime

# GPIO setup
relay_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)


def water(pin, level):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if level < 15:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin, GPIO.LOW)
        # write to logfile
        print(f"{now} - Lemon tree watered! Soil moisture was at {level}%")

        # send mail
        # image
        today = datetime.now().strftime("%d-%m-%Y")
        image_path = "/home/pi/lemon_pi/daily_picture/" + today + ".jpg"
        subject = f"Your lemon tree is healthy! Watered today. Soil moisture was at {level}%"
        SendMail(image_path, subject)

    else:
        print(f"{now} - No watering needed. Soil moisture is at {level}%")


# Check soil moisture level
_, _, soil_level = SoilMoistureLevel()

# Check if it needs watering
water(relay_pin, soil_level)

GPIO.cleanup()
