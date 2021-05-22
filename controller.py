import atexit
#import json
import logging
import math
#import mmap
import os
import signal
import sys

from datetime import datetime
from time import sleep

# Import application libraries ------------------------------------------------
import brewdb
import paths

from xchg import Xchg

class BrewfermController():
    def __init__(self):
        super().__init__()

        self.beer_temp = "00.0"
        self.beer_target = "00.0"
        self.desired_state = "cool"
        self.sensors_out = Xchg(paths.sensors_out, 'r', default={})
        self.relays_out = Xchg(paths.relays_out, 'r', default={})
        self.relays_in = Xchg(paths.relays_in, 'w', default={})
        self.relays_in.write({"desired":"idle"})


# main loop here
if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.DEBUG, filename='/home/pi/brewferm/logs/brewferm.log',format='%(asctime)s-%(process)d-controller.py -%(levelname)s-%(message)s')
        logging.debug("controller starting up")
        mycontroller = BrewfermController()
        
        count = 0
        while count < 6:
            count = count + 1
            #sensor_readings = mycontroller.read_mmap()
            sleep(300)

        
        logging.debug("readings = %s", sensor_readings)
    except Exception as e:
        logging.exception("%s %s", type(e), e)
