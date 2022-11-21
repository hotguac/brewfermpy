import sys

from time import sleep

# Import application libraries --------------------------------------
import killer
import paths

"""
Creates a rotating log, must be done prior
to import from pic or xchg in order for the
rotating function to work correctly.
Use   # noqa: E402 to have flake ignore module level
import after the 'logger = ' statement.
"""
from logger import BrewfermLogger
logger = BrewfermLogger('controller.py').getLogger()

from pid import BeerPID, ChamberPID  # noqa: E402
from xchg import XchgData  # noqa: E402

from datetime import timedelta, datetime  # noqa: E402


# -------------------------------------------------------------------
# Handles PID and sends desired to relays
# -------------------------------------------------------------------
class BrewfermController():
    def __init__(self):
        super().__init__()

        self.xd = XchgData(paths.controller_out)

        beer_target = self.xd.get(paths.beer_target)
        chamber_temp = self.xd.get(paths.chamber_temp)
        if (chamber_temp is None) or (beer_target is None):
            logger.info('not ready yet, exiting')
            sys.exit(0)

        self.beer_tuning = self.xd.get(paths.beerPID)
        self.chamber_tuning = self.xd.get(paths.chamberPID)

        self.desired_state = paths.idle

        self.beerPID = BeerPID(beer_target)
        self.beerPID.set_tuning(self.beer_tuning)
        self.beerPID.pid._last_output = beer_target
        self.beerPID.pid._integral = beer_target

        self.chamberPID = ChamberPID(beer_target)
        self.chamberPID.set_tuning(self.chamber_tuning)
        self.chamberPID.pid._last_output = 50
        self.chamberPID.pid._integral = 50

        self.last_output = datetime.now() - timedelta(minutes=3)
        self.calibrations = self.xd.get(paths.calibrations, {})

    def calculate(self):
        try:
            beer_target = self.xd.get(paths.beer_target)
            beer_temp = self.xd.get(paths.beer_temp) + self.xd.get(paths.beer_temp_offset, 0.0)
            chamber_temp = self.xd.get(paths.chamber_temp) + self.xd.get(paths.chamber_temp_offset, 0.0)

            if beer_target != self.beerPID.pid.setpoint:
                self.beerPID.change_target(beer_target)

            x = self.beerPID.update(beer_temp)
            self.chamberPID.pid.setpoint = x

            self.heat_cool = self.chamberPID.update(float(chamber_temp))
            ckp, cki, ckd = self.chamberPID.pid.components
            bkp, bki, bkd = self.beerPID.pid.components

            ts = datetime.now()
            if ts > (self.last_output + timedelta(minutes=2)):
                self.last_output = ts
                logger.info(
                    ' beer = c%.1f / t%.1f / I%.1f pi%s / st%s '
                    ' chamber = c%.1f / t%.1f / hc%.1f / I%.1f pi%s / st%s',
                    round(beer_temp, 2),
                    round(self.beerPID.pid.setpoint),
                    round(bki, 1),
                    (
                        self.beerPID.pid.tunings[0],
                        self.beerPID.pid.tunings[1]
                    ),
                    round(self.beerPID.pid.sample_time, 1),
                    round(chamber_temp, 2),
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
            logger.exception("%s %s", type(e), e)

    def output_desired(self):
        try:
            self.xd.write_controller({paths.desired: self.desired_state})
        except Exception as e:
            logger.exception("%s %s", type(e), e)

    def update(self):
        temp = self.xd.get(paths.beer_temp)
        if temp is None:
            beer_temp = None
        else:
            offset = self.xd.get(paths.beer_temp_offset, 0.0)
            beer_temp = temp + offset

        beer_target = self.xd.get(paths.beer_target)

        if (self.xd.get(paths.state, paths.paused) == paths.paused):
            self.desired_state = paths.paused
        else:
            if (beer_temp is None):
                self.desired_state = paths.paused
            else:
                self.calculate()

                if self.heat_cool > 80:
                    if ((beer_temp - beer_target) > 10):
                        self.desired_state = paths.idle
                    else:
                        self.desired_state = paths.heat
                else:
                    if self.heat_cool < 20:
                        self.desired_state = paths.cool
                    else:
                        self.desired_state = paths.idle

        beertuning = self.xd.get(paths.beerPID)
        chambertuning = self.xd.get(paths.chamberPID)

        if (beertuning is None) or (chambertuning is None):
            logger.warning(
                'beertuning = %s and chamber tuning = %s',
                beertuning, chambertuning)
            self.desired_state = paths.paused
        else:
            if beertuning != self.beer_tuning:
                self.beer_tuning = beertuning
                self.beerPID.set_tuning(self.beer_tuning)

            if chambertuning != self.chamber_tuning:
                self.chamber_tuning = chambertuning
                self.chamberPID.set_tuning(self.chamber_tuning)

        self.output_desired()


# -------------------------------------------------------------------
# main loop here
# -------------------------------------------------------------------
if __name__ == '__main__':
    try:
        logger.info("controller starting up")

        mycontroller = BrewfermController()
        killer = killer.GracefulKiller()

        while not killer.kill_now:
            mycontroller.update()
            sleep(4)

        logger.info('shutting down')
        sys.exit(0)

    except Exception as e:
        logger.exception("%s %s", type(e), e)
