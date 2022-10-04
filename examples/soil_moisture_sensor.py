import os
import sys
import time

sys.path.append('../')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from DFRobot_ADS1115 import ADS1115
ads1115 = ADS1115()

while True:
    # Set the IIC address
    ads1115.set_addr_ADS1115(0x49)
    # Get the Digital Value from selected channel
    adc0 = ads1115.read_voltage(0)
    value = adc0['r']
    # values are between 2700mV (Dry) and 1130mV (Wet) approximately
    normal = abs(value - 2700)/100
    # normalized values are between 0 and 16 approximately
    percnt = round((normal/16)*100, 2)
    time.sleep(0.2)
    print(f"mV: {value} | Normalized: {normal} | Percent: {percnt}")
