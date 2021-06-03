#!/usr/bin/python3
#""" PID clases configured for the beer and the chamber """
# Import standard libraries ---------------------------------------------------
import atexit
import logging
import RPi.GPIO as GPIO
import sys

from simple_pid import PID 

from time import sleep

# Import application libraries ------------------------------------------------
import paths
from xchg import Xchg

# Classes ------------------------------------------------------------
class BrewfermPID:
    def __init__(self, set_point):
        self.set_point = set_point
        self.pid = PID(1, 0.5, 0.01)
        self.auto_mode = True

    # Functions ------------------------------------------------------------
    def update(self, current_temp):
        return self.pid(current_temp)

class BeerPID:
    def __init__(self, set_point):      
        self.sample_time = 60.0 # seconds
        
        self.kp = 4.0
        self.ki = 0.2
        self.kd = 0.01

        self.set_point = set_point
        self.pid = PID(set_point)
        self.pid.sample_time = 60
        self.pid.tunings = self.kp, self.ki, self.kd
        self.pid.output_limits = self.set_point - 10, self.set_point + 10

    def update(self, current_temp):
        self.pid.output_limits = float(current_temp) - 10.0, float(current_temp) + 6.0
        return self.pid(current_temp)

    def change_target(self, target):
        self.set_point = target
        self.pid.set_point = self.set_point
      
class ChamberPID:
    def __init__(self, set_point):
        
        self.kp = 6.0
        self.ki = 0.2
        self.kd = 0.01

        self.pid = PID(50)
        self.pid.sample_time = 30.0 # seconds
        self.pid.tunings = self.kp, self.ki, self.kd
        self.pid.output_limits = 0, 10

    def change_target(self, target):
        self.set_point = target
        self.pid.set_point = self.set_point
      
    def update(self, current_temp):
        try:
            x = current_temp
            self.pid.output_limits = x - 10.0, x + 6.0
        except Exception as e:
            logging.exception('%s %s', type(e), e)

        return self.pid(float(current_temp))


# main loop here
if __name__ == '__main__':
    try:
        logging.basicConfig(
            level=logging.DEBUG, filename=paths.logs, 
            format='%(asctime)s-%(process)d-pid.py  -%(levelname)s-%(message)s')
        
        logging.info("running BrewfermPID module tests")
        logging.info("finished BrewfermPID module tests")

    except Exception as e:
        logging.exception("%s %s", type(e), e)
