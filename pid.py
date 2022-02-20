#!/usr/bin/python3
# """ PID clases configured for the beer and the chamber """

# Import standard libraries ---------------------------------------------------
import logging

from simple_pid import PID

# Import application libraries ------------------------------------------------
import paths


# Classes ------------------------------------------------------------
class BeerPID:
    def __init__(self, setpoint):
        self.sample_time = 60.0  # seconds

        self.kp = 6.0  # these should get overwriten quickly
        self.ki = 0.8
        self.kd = 0.01

        self.setpoint = setpoint

        low_limit = setpoint - 20
        if low_limit < 34:
            low_limit = 34

        high_limit = setpoint + 4
        if high_limit > 84:
            high_limit = 84

        self.pid = PID(
            Kp=self.kp,
            Ki=self.ki,
            Kd=self.kd,
            sample_time=2,
            output_limits=(low_limit, high_limit),
            setpoint=self.setpoint)

    def update(self, current_temp):
        # TODO: refactor the limits from here, init, and change_target
        if (current_temp - self.setpoint) > 2:
            low_limit = self.setpoint - 20
            if low_limit < 34:
                low_limit = 34
        else:
            old_low = self.pid.output_limits[0]
            low_limit = ((self.setpoint - 8) + (old_low * 89)) / 90

            if low_limit < 34:
                low_limit = 34

        high_limit = self.pid.output_limits[1]
        self.pid.output_limits = low_limit, high_limit

        # logging.info('current = %s limits = %s', current_temp, self.pid.output_limits)
        return self.pid(current_temp)

    def change_target(self, setpoint):
        # TODO: the low limit is wrong!! get from controller
        low_limit = setpoint - 6
        if low_limit < 34:
            low_limit = 34

        high_limit = setpoint + 4
        if high_limit > 84:
            high_limit = 84

        if setpoint != self.setpoint:
            self.setpoint = setpoint
            self.pid.output_limits = low_limit, high_limit
            self.pid.setpoint = self.setpoint
            self.pid._integral = setpoint
            self.pid._last_output = setpoint

        logging.info(
            'new beer target %s with limits %s',
            self.pid.setpoint,
            self.pid.output_limits
            )

    def get_tuning(self):
        try:
            x = {}
            x['kp'] = self.kp
            x['ki'] = self.ki
            x['kd'] = self.kd
            x['sample_time'] = self.pid.sample_time
            return x
        except Exception as e:
            logging.exception('%s %s', type(e), e)

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
            logging.exception('%s %s', type(e), e)


class ChamberPID:
    def __init__(self, setpoint):
        self.kp = 2.0
        self.ki = 0.01
        self.kd = 0.000001

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
            logging.exception('%s %s', type(e), e)

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
            logging.exception('%s %s', type(e), e)


# main loop here
if __name__ == '__main__':
    try:
        logging.basicConfig(
            level=logging.DEBUG, filename=paths.logs,
            format=(
                '%(asctime)s-%(process)d-pid.py  '
                '-%(levelname)s-%(message)s'))

        logging.info("running BrewfermPID module tests")
        logging.info("finished BrewfermPID module tests")

    except Exception as e:
        logging.exception("%s %s", type(e), e)
