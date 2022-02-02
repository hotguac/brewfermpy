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
    def __init__(self, cool_pin, heat_pin):
        self.cool_pin = cool_pin
        self.heat_pin = heat_pin
        self.setup_gpio()
        self.sleep_time = 30  # 2
        self.timeout = False

        start_time = datetime.now()

        self.heat_off = start_time
        self.cool_off = start_time
        self.heat_on = start_time
        self.cool_on = start_time

        self.xd = XchgData(paths.relays_out)
        self.current_state = paths.idle

        self.off_on = 6  # minutes
        self.max_on = 7  # minutes
        self.min_on = 1  # minutes

        self.hc_balance = 4  # multiply times for heat

    # Functions ------------------------------------------------------------
    def setup_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.cool_pin, GPIO.OUT)
        GPIO.output(self.cool_pin, GPIO.LOW)
        GPIO.setup(self.heat_pin, GPIO.OUT)
        GPIO.output(self.heat_pin, GPIO.LOW)
        GPIO.setwarnings(True)

    def gpio_cleanup(self):
        logging.info('releasing GPIO')
        GPIO.output(self.heat_pin, GPIO.LOW)
        GPIO.output(self.cool_pin, GPIO.LOW)
        GPIO.cleanup()

    def last_turned_off(self):
        if self.heat_off > self.cool_off:
            return self.heat_off
        else:
            return self.cool_off

    def check_min_max(self, desired_state):
        # logging.debug('current_state = %s desired = %s', self.current_state, desired_state)
        now = datetime.now()
        last_off = self.last_turned_off()

        if self.current_state == paths.idle:
            if (desired_state == paths.idle) or (desired_state == paths.paused):
                return desired_state

            wait_time = timedelta(minutes=self.off_on)
            if (now < (last_off + wait_time)):
                return paths.idle

            if desired_state == paths.heat:
                self.heat_on = now
                return desired_state
            else:
                self.cool_on = now
                return desired_state

        if (self.current_state == paths.heat):
            if (desired_state == paths.paused):
                self.heat_off = now
                return desired_state

            min_time = timedelta(minutes=(self.min_on))
            if (now < (self.heat_on + min_time)):
                return paths.heat

            max_time = timedelta(minutes=(self.max_on * self.hc_balance))
            if ((desired_state == paths.heat) and (now < (self.heat_on + max_time))):
                return desired_state

            self.heat_off = now
            return paths.idle

        if (self.current_state == paths.cool):
            if (desired_state == paths.paused):
                self.cool_off = now
                return desired_state

            min_time = timedelta(minutes=(self.min_on))
            if now < (self.cool_on + min_time):
                return paths.cool

            max_time = timedelta(minutes=(self.max_on))
            if ((desired_state == paths.cool) and (now < (self.cool_on + max_time))):
                return desired_state

            self.cool_off = now
            return paths.idle

        if (self.current_state == paths.paused):
            if (self.xd.get(paths.state) == paths.running) and (desired_state != paths.paused):
                return paths.idle
            else:
                return paths.paused

    def timed_out(self, desired_ts):
        # pause system if controller isn't updating desired state
        last_update = parser.parse(desired_ts)
        if last_update < (datetime.now() - timedelta(minutes=2)):
            self.sleep_time = 6
            self.timeout = True
        else:
            if self.timeout:
                logging.info('found controller output, resuming...')
                self.timeout = False
                self.sleep_time = 2

        return self.timeout

    def update(self):
        try:
            desired_state = self.xd.get(paths.desired, default=paths.idle)
            expired_ts = (datetime.now() - timedelta(minutes=20))
            ts = self.xd.get('desired_ts', default=str(expired_ts))
        except Exception as e:
            logging.exception('input mmap not ready %s %s', type(e), e)
            sys.exit(1)
        else:
            if self.timed_out(ts):
                desired_state = paths.paused
                if self.current_state != paths.paused:
                    logging.warning('old or missing controller output, going to pause')

            # do more checks here to see if timers passed for state change
            new_state = self.check_min_max(desired_state)

            if new_state != self.current_state:
                logging.info('old = %s current = %s', self.current_state, new_state)
                self.current_state = new_state

            if self.current_state is None:
                self.current_state = paths.idle

    def implement_current(self):
        try:
            if self.current_state == paths.heat:
                GPIO.output(self.cool_pin, GPIO.LOW)
                GPIO.output(self.heat_pin, GPIO.HIGH)
            if self.current_state == paths.cool:
                GPIO.output(self.heat_pin, GPIO.LOW)
                GPIO.output(self.cool_pin, GPIO.HIGH)
            if self.current_state == paths.idle:
                GPIO.output(self.heat_pin, GPIO.LOW)
                GPIO.output(self.cool_pin, GPIO.LOW)
            if self.current_state == paths.paused:
                GPIO.output(self.heat_pin, GPIO.LOW)
                GPIO.output(self.cool_pin, GPIO.LOW)

            self.xd.write_relays({"current": self.current_state})
        except Exception as e:
            logging.exception('%s %s', type(e), e)
            sys.exit(1)


# main loop here
if __name__ == '__main__':
    try:
        logging.basicConfig(
            level=logging.DEBUG, filename=paths.logs,
            format=(
                '%(asctime)s-%(process)d-relays.py  '
                '-%(levelname)s-%(message)s'))

        logging.info("relays starting up")
        myrelays = BrewfermRelays(12, 16)  # BCM pin 18

        atexit.register(myrelays.gpio_cleanup)

        killer = killer.GracefulKiller()
        while not killer.kill_now:
            myrelays.update()
            myrelays.implement_current()
            sleep(myrelays.sleep_time)

    except Exception as e:
        logging.exception("%s %s", type(e), e)

sleep(10)
logging.info('clean exit')
sys.exit(0)
