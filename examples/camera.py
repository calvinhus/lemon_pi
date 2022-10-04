#!/usr/bin/env python

from picamera import PiCamera

camera = PiCamera()
camera.capture('/home/pi/lemon_pi/static/images/picture_test.jpg')
