import time
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
sensor = adafruit_dht.DHT11(board.D23)

# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# sensor = adafruit_dht.DHT22(board.D18, use_pulseio=False)

while True:
    try:
        # Print the values to the serial port
        temperature = sensor.temperature
        humidity = sensor.humidity
        print(f"Temp: {temperature}C    Humidity: {humidity}% ")

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(2.0)
