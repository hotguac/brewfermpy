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

        self.beer_target = self.xd.get(paths.beer_target)
        self.chamber_temp = self.xd.get(paths.chamber_temp)
        if (self.chamber_temp is None) or (self.beer_target is None):
            logging.info('not ready yet, exiting')
            sys.exit(0)

        self.beer_temp = self.xd.get(paths.beer_temp)
        self.beer_tuning = self.xd.get(paths.beerPID)
        self.chamber_tuning = self.xd.get(paths.chamberPID)

        self.desired_state = paths.idle

        self.beerPID = BeerPID(self.beer_target)
        self.beerPID.set_tuning(self.beer_tuning)
        self.beerPID.pid._last_output = self.beer_target
        self.beerPID.pid._integral = self.beer_target

        self.chamberPID = ChamberPID(self.beer_target)
        self.chamberPID.set_tuning(self.chamber_tuning)
        self.chamberPID.pid._last_output = 50
        self.chamberPID.pid._integral = 50

        self.last_output = datetime.now() - timedelta(minutes=3)

    def calculate(self):
        try:
            beer_target = self.xd.get(paths.beer_target)

            if beer_target != self.beerPID.pid.setpoint:
                self.beerPID.change_target(beer_target)

            x = self.beerPID.update(self.beer_temp)
            self.chamberPID.pid.setpoint = x

            self.heat_cool = self.chamberPID.update(float(self.chamber_temp))
            ckp, cki, ckd = self.chamberPID.pid.components
            bkp, bki, bkd = self.beerPID.pid.components

            ts = datetime.now()
            if ts > (self.last_output + timedelta(minutes=2)):
                self.last_output = ts
                logging.debug(
                    ' beer = %.1f / %.1f / %.1f %s / %s '
                    ' chamber = %.1f / %.1f / %.1f / %.1f %s / %s',
                    round(self.beer_temp, 2),
                    round(self.beerPID.pid.setpoint),
                    round(bki, 1),
                    (
                        self.beerPID.pid.tunings[0],
                        self.beerPID.pid.tunings[1]
                    ),
                    round(self.beerPID.pid.sample_time, 1),
                    round(self.chamber_temp, 2),
                    round(x, 1),
                    round(self.heat_cool, 2),
                    round(cki, 1),
                    (
                        self.chamberPID.pid.tunings[0],
                        self.chamberPID.pid.tunings[1]
                    ),
                    round(self.chamberPID.pid.sample_time, 1)
                )
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def output_desired(self):
        try:
            self.xd.write_controller({paths.desired: self.desired_state})
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def update(self):
        self.beer_temp = self.xd.get(paths.beer_temp)
        self.chamber_temp = self.xd.get(paths.chamber_temp)

        if self.xd.get(paths.state, paths.paused) == paths.paused:
            self.desired_state = paths.paused
        else:
            self.calculate()
            self.desired_state = paths.idle

            if self.heat_cool > 80:
                self.desired_state = paths.heat
            if self.heat_cool < 20:
                self.desired_state = paths.cool

        beertuning = self.xd.get(paths.beerPID)
        chambertuning = self.xd.get(paths.chamberPID)

        if (beertuning is None) or (chambertuning is None):
            logging.debug(
                'beertuning = %s and chamber tuning = %s',
                beertuning, chambertuning)
            self.desired_state = paths.paused
        else:
            if beertuning != self.beer_tuning:
                logging.debug(
                    'old beer tuning %s vs new %s',
                    beertuning,
                    self.beer_tuning)
                self.beer_tuning = beertuning
                self.beerPID.set_tuning(self.beer_tuning)

            if chambertuning != self.chamber_tuning:
                logging.debug(
                    'old chamber tuning %s vs new %s',
                    chambertuning,
                    self.chamber_tuning)
                self.chamberPID.set_tuning(self.chamber_tuning)

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
