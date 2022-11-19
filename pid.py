#!/usr/bin/python3
# """ PID clases configured for the beer and the chamber """

# Import standard libraries ---------------------------------------------------
from simple_pid import PID

# Import application libraries ------------------------------------------------
from logger import BrewfermLogger
import paths


"""
Creates a rotating log
"""
logger = BrewfermLogger('pid.py').getLogger()


# Classes ------------------------------------------------------------
class BeerPID:
    def __init__(self, setpoint):
        self.sample_time = 60.0  # seconds

        # these are defaults that will be
        # overwritten by any user stored values
        self.kp = paths.default_beerP
        self.ki = paths.default_beerI
        self.kd = paths.default_beerD

        self.setpoint = setpoint

        self.pid = PID(
            Kp=self.kp,
            Ki=self.ki,
            Kd=self.kd,
            sample_time=2,
            output_limits=self.calculate_limits(setpoint),
            setpoint=self.setpoint)

        logger.info(
            'new beer target %s with limits %s',
            self.pid.setpoint,
            self.pid.output_limits)

    def calculate_limits(self, current_temp):
        if current_temp > (self.setpoint + 2):
            low_limit = self.setpoint - paths.beer_lowlimit_offset
        else:
            low_limit = self.setpoint - (paths.beer_lowlimit_offset * 0.6)

        if current_temp < (self.setpoint - 2):
            high_limit = self.setpoint + paths.beer_highlimit_offset
        else:
            high_limit = self.setpoint + (paths.beer_highlimit_offset * 0.6)

        if low_limit < paths.beer_lowlimit_low:
            low_limit = paths.beer_lowlimit_low

        if high_limit > paths.beer_highlimit_high:
            high_limit = paths.beer_highlimit_high

        return low_limit, high_limit

    def update(self, current_temp):
        self.pid.output_limits = self.calculate_limits(current_temp)

        return self.pid(current_temp)

    def change_target(self, setpoint):
        if setpoint != self.setpoint:
            self.setpoint = setpoint
            self.pid.output_limits = self.calculate_limits(setpoint)
            self.pid.setpoint = self.setpoint
            self.pid._integral = setpoint
            self.pid._last_output = setpoint

    def get_tuning(self):
        try:
            x = {}
            x['kp'] = self.kp
            x['ki'] = self.ki
            x['kd'] = self.kd
            x['sample_time'] = self.pid.sample_time
            return x
        except Exception as e:
            logger.exception('%s %s', type(e), e)

    def set_tuning(self, new_settings):
        try:
            if new_settings.get('kp') is not None:
                self.kp = new_settings['kp']

            if new_settings.get('ki') is not None:
                self.ki = new_settings['ki']

            if new_settings.get('kd') is not None:
                self.kd = new_settings['kd']

            self.pid.tunings = self.kp, self.ki, self.kd

            if new_settings.get('sample_time') is not None:
                self.pid.sample_time = new_settings['sample_time']
        except Exception as e:
            logger.exception('%s %s', type(e), e)


class ChamberPID:
    def __init__(self, setpoint):
        # these are defaults that will be
        # overwritten by any user stored values
        self.kp = paths.default_chamberP
        self.ki = paths.default_chamberI
        self.kd = paths.default_chamberD

        self.setpoint = setpoint
        self.pid = PID(
            Kp=self.kp,
            Ki=self.ki,
            Kd=self.kd,
            sample_time=2,
            output_limits=(1, 100),
            setpoint=self.setpoint)

        self._integral = 50
        self._last_output = 50

    def update(self, current_temp):
        return self.pid(float(current_temp))

    def get_tuning(self):
        try:
            x = {}
            x['kp'] = self.kp
            x['ki'] = self.ki
            x['kd'] = self.kd
            x['sample_time'] = self.pid.sample_time
            return x
        except Exception as e:
            logger.exception('%s %s', type(e), e)

    def set_tuning(self, new_settings):
        try:
            if new_settings.get('kp') is not None:
                self.kp = new_settings['kp']

            if new_settings.get('ki') is not None:
                self.ki = new_settings['ki']

            if new_settings.get('kd') is not None:
                self.kd = new_settings['kd']

            self.pid.tunings = self.kp, self.ki, self.kd

            if new_settings.get('sample_time') is not None:
                self.pid.sample_time = new_settings['sample_time']

        except Exception as e:
            logger.exception('%s %s', type(e), e)


# main loop here
if __name__ == '__main__':
    try:
        logger.info("running BrewfermPID module tests")
        logger.info("finished BrewfermPID module tests")

    except Exception as e:
        logger.exception("%s %s", type(e), e)
