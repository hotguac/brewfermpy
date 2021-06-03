#!/usr/bin/python3
""" Enforces cycle time while turning relays on and off """

# Import standard libraries ---------------------------------------------------
import atexit
import logging
import RPi.GPIO as GPIO
import sys

from time import sleep

# Import application libraries ------------------------------------------------
import paths
from xchg import Xchg

# Classes ------------------------------------------------------------
class BrewfermRelays:
    def __init__(self, pin_number):
        self.pin = pin_number
        self.current_state = "heat"
        self.setup_gpio()
        self.xchg_in = Xchg(paths.relays_in, mode='r', default={"desired":"idle"})
        self.xchg_out = Xchg(paths.relays_out, mode='w', default={"desired":"idle"})

    # Functions ------------------------------------------------------------
    def setup_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        GPIO.output(18, GPIO.HIGH)
        GPIO.setwarnings(True)

    def gpio_cleanup(self):
        logging.info('releasing GPIO')
        GPIO.cleanup()

    def update(self):
        self.desired = self.xchg_in.read()
        
        if self.current_state == "heat":
            self.current_state = "cool"
        else: 
            if self.current_state == "cool":
                self.current_state = "idle"
            else:
                self.current_state = "heat"

        self.xchg_out.write({"current":self.current_state})

# main loop here
if __name__ == '__main__':
    try:
        logging.basicConfig(
            level=logging.DEBUG, filename=paths.logs, 
            format='%(asctime)s-%(process)d-relays.py  -%(levelname)s-%(message)s')
        
        logging.info("relays starting up")
        myrelays = BrewfermRelays(18) # BCM pin 18
        
        atexit.register(myrelays.gpio_cleanup)
        
        count = 0
        while count < 600:
            count = count + 1
            myrelays.update()
            sleep(2)
     
    except Exception as e:
        logging.exception("%s %s", type(e), e)

sys.exit(1)
