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
from xchg import XchgData

# Classes ------------------------------------------------------------
class BrewfermRelays:
    def __init__(self, pin_number):
        self.pin = pin_number
        self.current_state = "idle"
        self.desired_state = None
        self.setup_gpio()
        self.xd = XchgData(paths.relays_out)
        self.sleep_time = 2
        self.timeout = False

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
        keep_alive = 2
        ka_ts = datetime.now() - timedelta(minutes=keep_alive)          

        try:
            self.desired_state = self.xd.get('desired')
            self.desired_ts = self.xd.get('desired_ts')

            # pause system if controller isn't updating desired state
            if (self.desired_state is None) or (self.desired_ts is None):
                if self.current_state != paths.paused:
                    logging.warning('missing controller output, going to pause')
                self.desired_state = paths.paused
                self.sleep_time = 10
                self.timeout = True
            else:
                x = parser.parse(self.desired_ts)
                if x < ka_ts:
                    if self.current_state != paths.paused:
                        logging.warning('old controller output, going to pause')
                    self.desired_state = paths.paused
                    self.sleep_time = 10
                    self.timeout = True
                else:
                    if self.timeout:
                        logging.info('found controller output, resuming...')
                        self.timeout = False
                    self.sleep_time = 2
                    
        except Exception as e:
            logging.exception('input mmap not ready %s %s', type(e), e)
            sys.exit(1)
            
        if self.desired_state == paths.paused:
            self.current_state = self.desired_state
        else:
            # do more checks here to see if timers passed for state change
            self.current_state = self.desired_state
                        
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
