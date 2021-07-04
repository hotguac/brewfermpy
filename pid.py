#!/usr/bin/python3
# """ PID clases configured for the beer and the chamber """

# Import standard libraries ---------------------------------------------------
import logging

from simple_pid import PID

# Import application libraries ------------------------------------------------
import paths


# Classes ------------------------------------------------------------
class BeerPID:
    def __init__(self, set_point):
        self.sample_time = 60.0  # seconds

        self.kp = 6.0  # these should get overwriten quickly
        self.ki = 0.8
        self.kd = 0.01

        self.set_point = set_point

        low_limit = set_point - 6
        if low_limit < 34:
            low_limit = 34

        high_limit = set_point + 4
        if high_limit > 84:
            high_limit = 84

        self.pid = PID(
            Kp=self.kp,
            Ki=self.ki,
            Kd=self.kd,
            sample_time=2,
            output_limits=(low_limit, high_limit),
            setpoint=self.set_point)

    def update(self, current_temp):
        # logging.debug('beer tuning = %s', self.pid.tunings)
        return self.pid(current_temp)

    def change_target(self, set_point):
        low_limit = set_point - 6
        if low_limit < 34:
            low_limit = 34

        high_limit = set_point + 4
        if high_limit > 84:
            high_limit = 84

        if set_point != self.set_point:
            self.set_point = set_point
            self.pid.output_limits = low_limit, high_limit
            self.pid.set_point = self.set_point
            self.pid._integral = set_point
            self.pid._last_output = set_point

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

            # logging.debug('now tuned to %s', self.get_tuning())
        except Exception as e:
            logging.exception('%s %s', type(e), e)


class ChamberPID:
    def __init__(self, set_point):
        self.kp = 2.0
        self.ki = 0.01
        self.kd = 0.000001

        self.set_point = set_point
        self.pid = PID(
            Kp=self.kp,
            Ki=self.ki,
            Kd=self.kd,
            sample_time=2,
            output_limits=(1, 100),
            setpoint=self.set_point)

        self._integral = 50
        self._last_output = 50

    # def change_target(self, target):
    #     if target != self.set_point:
    #         self.set_point = target
    #         self.pid.set_point = self.set_point
    #         # logging.debug('chamber PID tuning = %s and set point = %s', self.pid.tunings, target)

    def update(self, current_temp):
        # logging.debug('chamber PID tuning = %s', self.pid.tunings)
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
        # logging.debug('chamber set tuning to %s', new_settings)
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
