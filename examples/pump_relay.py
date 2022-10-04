import RPi.GPIO as GPIO
import time

pin = 17

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

def pump_on(pin):
    GPIO.output(pin, GPIO.HIGH)


def pump_off(pin):
    GPIO.output(pin, GPIO.LOW)


pump_on(pin)
time.sleep(2)
pump_off(pin)
GPIO.cleanup()
