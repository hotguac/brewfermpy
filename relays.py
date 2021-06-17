#!/usr/bin/python3
""" Enforces cycle time while turning relays on and off """

# Import standard libraries ---------------------------------------------------
import atexit
import logging
import RPi.GPIO as GPIO
import sys

from datetime import timedelta, datetime
from dateutil import parser
from time import sleep

# Import application libraries ------------------------------------------------
import killer
import paths
from xchg import Xchg, XchgData

# Classes ------------------------------------------------------------
class BrewfermRelays:
    def __init__(self, pin_number):
        self.pin = pin_number
        self.current_state = "idle"
        self.desired_state = None
        self.setup_gpio()
        self.xd = XchgData(paths.relays_out)
        self.sleep_time = 2

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
        try:
            self.desired = self.xd.get_desired_state()
            self.desired_ts = self.xd.get_desired_ts()    

            # pause system if controller isn't updating desired state
            if (self.desired is None) or (self.desired_ts is None):
                self.desired = paths.paused
                self.current = paths.paused
                self.sleep_time = 20
                return

            keep_alive = 2
            if parser.parse(self.desired_ts) < datetime.now() - timedelta(minutes=keep_alive):
                self.desired = paths.paused
                self.current = paths.paused
                self.sleep_time = 20
                return

            self.sleep_time = 2
            self.current = self.desired
                    
        except Exception as e:
            logging.exception('input mmap not ready %s %s', type(e), e)
            sys.exit(1)
            
        try:
            self.current_state = self.desired
        except Exception as e:
            logging.exception('%s %s', type(e), e)
            sys.exit(1)
                        
    def post_current(self):
        try:
            self.xd.write_relays({"current":self.current_state})
        except Exception as e:
            logging.exception('%s %s', type(e), e)

# main loop here
if __name__ == '__main__':
    try:
        logging.basicConfig(
            level=logging.DEBUG, filename=paths.logs, 
            format='%(asctime)s-%(process)d-relays.py  -%(levelname)s-%(message)s')
        
        logging.info("relays starting up")
        myrelays = BrewfermRelays(18) # BCM pin 18
        
        atexit.register(myrelays.gpio_cleanup)
        
        killer = killer.GracefulKiller()
        while not killer.kill_now:
            myrelays.update()
            myrelays.post_current()
            sleep(myrelays.sleep_time)
     
    except Exception as e:
        logging.exception("%s %s", type(e), e)

sleep(10)
logging.info('clean exit')
sys.exit(0)
