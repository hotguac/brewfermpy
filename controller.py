import logging
import sys

from time import sleep

# Import application libraries --------------------------------------
import killer
import paths

from pid import BeerPID, ChamberPID
from xchg import XchgData

from datetime import timedelta, datetime


# -------------------------------------------------------------------
# Handles PID and sends desired to relays
# -------------------------------------------------------------------
class BrewfermController():
    def __init__(self):
        super().__init__()

        self.xd = XchgData(paths.controller_out)
        self.beer_temp = self.xd.get('beer')
        self.chamber_temp = self.xd.get('chamber')
        self.beer_target = self.xd.get('target')
        self.current_state = self.xd.get('current', paths.paused)
        self.desired_state = paths.idle

        self.beerPID = BeerPID(self.beer_target)
        self.beerPID._last_output = self.beer_target
        self.beerPID._integral = self.beer_target
        self.chamberPID = ChamberPID(self.beer_target)

        self.beerPID_tuning = self.xd.get('beer_pid')
        self.beerPID.set_tuning(self.beerPID_tuning)

        self.chamberPID_tuning = self.xd.get('chamber_pid')
        self.chamberPID._last_output = 50
        self.chamberPID._integral = 50
        self.chamberPID.set_tuning(self.chamberPID_tuning)

        self.last_output = datetime.now() - timedelta(minutes=3)

    def calculate(self):
        try:
            x = self.beerPID.update(self.beer_temp)
            self.chamberPID.change_target(x)
            self.heat_cool = self.chamberPID.update(float(self.chamber_temp))

            ts = datetime.now()
            if ts > (self.last_output + timedelta(minutes=1, seconds=20)):
                self.last_output = ts
                logging.debug(
                    'beer = %s target = %s /'
                    ' chamber = %s target = %s / control = %s',
                    round(self.beer_temp, 2),
                    round(self.beer_target),
                    round(self.chamber_temp, 2),
                    round(x, 2),
                    round(self.heat_cool, 2)
                )
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def output_desired(self):
        try:
            self.xd.write_controller({paths.desired: self.desired_state})
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def update(self):
        self.beer_temp = self.xd.get('beer')
        self.chamber_temp = self.xd.get('chamber')
        self.beer_target = self.xd.get('target')
        self.current_state = self.xd.get('current')

        if self.xd.get('paused_state', paths.paused) == paths.paused:
            self.desired_state = paths.paused
        else:
            self.calculate()
            self.desired_state = paths.idle

            if self.heat_cool > 80:
                self.desired_state = paths.heat
            if self.heat_cool < 20:
                self.desired_state = paths.cool

        beertuning = self.xd.get('beer_pid')
        chambertuning = self.xd.get('chamber_pid')

        if (beertuning is None) or (chambertuning is None):
            logging.debug(
                'beertuning = % s and chamber tuning = %s',
                beertuning,
                chambertuning)
            self.desired_state = paths.paused
        else:
            if beertuning != self.beerPID_tuning:
                logging.debug(
                    'old beer tuning %s vs new %s',
                    beertuning,
                    self.beerPID_tuning)
                self.beerPID.set_tuning(self.beerPID_tuning)

            if chambertuning != self.chamberPID_tuning:
                self.chamberPID.set_tuning(self.chamberPID_tuning)

        self.output_desired()


# -------------------------------------------------------------------
# main loop here
# -------------------------------------------------------------------
if __name__ == '__main__':
    try:
        logging.basicConfig(
            level=logging.DEBUG, filename=paths.logs,
            format=(
                '%(asctime)s-%(process)d-controller.py -'
                '%(levelname)s-%(message)s'))

        logging.info("controller starting up")

        mycontroller = BrewfermController()
        killer = killer.GracefulKiller()

        while not killer.kill_now:
            mycontroller.update()
            sleep(4)

        logging.info('shutting down')
        sys.exit(0)

    except Exception as e:
        logging.exception("%s %s", type(e), e)
