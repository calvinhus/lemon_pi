#!/usr/bin/env python

from picamera import PiCamera
from datetime import datetime

path = "/home/pi/lemon_pi/daily_picture/"
timestamp = datetime.now().strftime("%d-%m-%Y")
full_path = path + timestamp + ".jpg"

camera = PiCamera()
camera.capture(full_path)
