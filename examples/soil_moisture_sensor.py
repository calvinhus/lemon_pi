import os
import sys
import time

sys.path.append('../')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from DFRobot_ADS1115 import ADS1115
ads1115 = ADS1115()

while True:
    # Set the IIC address
    ads1115.set_addr_ADS1115(0x48)
    # Get the Digital Value from selected channel
    adc0 = ads1115.read_voltage(0)
    time.sleep(0.2)
    print(f"Channel 0: {adc0['r']} mV")
