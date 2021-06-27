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
        self.setup_gpio()
        self.sleep_time = 2
        self.timeout = False

        start_time = datetime.now()

        self.heat_off = start_time
        self.cool_off = start_time
        self.heat_on = start_time
        self.cool_on = start_time

        self.xd = XchgData(paths.relays_out)
        self.current_state = paths.idle
        self.desired_state = None

        self.off_on = 6  # minutes
        self.max_on = 6  # minutes
        self.min_on = 1  # minutes

        self.hc_balance = 4  # multiply times for heat

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

    def timed_out(self):
        if self.current_state != paths.paused:
            logging.warning(
                'old or missing controller output, going to pause')
        self.desired_state = paths.paused
        self.current_state = paths.paused
        self.sleep_time = 10
        self.timeout = True

    def check_timers(self):
        check_time = datetime.now()

        if self.heat_off > self.cool_off:
            last_off = self.heat_off
        else:
            last_off = self.cool_off

        if self.current_state == paths.idle:
            if self.desired_state == paths.idle:
                return paths.idle

            if last_off > (check_time - timedelta(minutes=self.off_on)):
                return paths.idle

            if self.desired_state == paths.heat:
                self.heat_on = check_time
            if self.desired_state == paths.cool:
                self.cool_on = check_time

            return self.desired_state

        if (self.current_state == paths.heat):
            tdelta = timedelta(minutes=(self.min_on))
            if (check_time < (self.heat_on + tdelta)):
                return paths.heat

            tdelta = timedelta(minutes=(self.max_on * self.hc_balance))
            if ((self.desired_state == paths.heat) and
                    (check_time < (self.heat_on + tdelta))):
                return paths.heat

            self.heat_off = check_time
            return paths.idle

        if (self.current_state == paths.cool):
            tdelta = timedelta(minutes=(self.min_on))
            if check_time < (self.cool_on + tdelta):
                return paths.cool

            tdelta = timedelta(minutes=(self.max_on))
            if ((self.desired_state == paths.cool) and
                    (check_time < (self.cool_on + tdelta))):
                return paths.cool

            self.cool_off = check_time
            return paths.idle

        if (self.current_state == paths.paused):
            return paths.paused

    def update(self):
        try:
            self.desired_state = self.xd.get('desired', default=paths.idle)

            expired = (datetime.now() - timedelta(minutes=20))
            self.desired_ts = self.xd.get(
                'desired_ts',
                default=str(expired))

            # pause system if controller isn't updating desired state
            last_update = parser.parse(self.desired_ts)
            if last_update < (datetime.now() - timedelta(minutes=2)):
                self.timed_out()
            else:
                if self.timeout:
                    logging.info('found controller output, resuming...')
                    self.timeout = False
                self.sleep_time = 2

        except Exception as e:
            logging.exception('input mmap not ready %s %s', type(e), e)
            sys.exit(1)
        else:
            # do more checks here to see if timers passed for state change
            old_current = self.current_state
            self.current_state = self.check_timers()

            if old_current != self.current_state:
                logging.info(
                    'old = %s current = %s',
                    old_current,
                    self.current_state)

            if self.current_state is None:
                self.current_state = paths.idle

    def post_current(self):
        try:
            self.xd.write_relays({"current": self.current_state})
        except Exception as e:
            logging.exception('%s %s', type(e), e)


# main loop here
if __name__ == '__main__':
    try:
        logging.basicConfig(
            level=logging.DEBUG, filename=paths.logs,
            format=(
                '%(asctime)s-%(process)d-relays.py  '
                '-%(levelname)s-%(message)s'))

        logging.info("relays starting up")
        myrelays = BrewfermRelays(18)  # BCM pin 18

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
