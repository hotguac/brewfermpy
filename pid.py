#!/usr/bin/python3
#""" PID clases configured for the beer and the chamber """

# Import standard libraries ---------------------------------------------------
import logging

from simple_pid import PID 

# Import application libraries ------------------------------------------------
import paths

# Classes ------------------------------------------------------------
class BeerPID:
    def __init__(self, set_point):      
        self.sample_time = 60.0 # seconds
        
        self.kp = 4.0
        self.ki = 0.2
        self.kd = 0.01

        self.set_point = set_point
        self.pid = PID(set_point)
        self.pid.sample_time = 60
        self.pid.tunings = self.kp, self.ki, self.kd
        self.pid.output_limits = self.set_point - 10, self.set_point + 10

    def update(self, current_temp):
        self.pid.output_limits = float(current_temp) - 10.0, float(current_temp) + 6.0
        return self.pid(current_temp)

    def change_target(self, target):
        self.set_point = target
        self.pid.set_point = self.set_point
      
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
                self.kp = new_settings['ki']
                
            if new_settings.get('kd') is not None:
                self.kp = new_settings['kd']
                
            self.pid.tunings = self.kp, self.ki, self.kd

            if new_settings.get('sample_time') is not None:
                self.pid.sample_time = new_settings['sample_time']

        except Exception as e:
            logging.exception('%s %s', type(e), e)

class ChamberPID:
    def __init__(self, set_point):
        
        self.kp = 6.0
        self.ki = 0.2
        self.kd = 0.01

        self.pid = PID(50)
        self.pid.sample_time = 30.0 # seconds
        self.pid.tunings = self.kp, self.ki, self.kd
        self.pid.output_limits = 0, 10

    def change_target(self, target):
        self.set_point = target
        self.pid.set_point = self.set_point
      
    def update(self, current_temp):
        try:
            x = current_temp
            self.pid.output_limits = x - 10.0, x + 6.0
        except Exception as e:
            logging.exception('%s %s', type(e), e)

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
                self.kp = new_settings['ki']
                
            if new_settings.get('kd') is not None:
                self.kp = new_settings['kd']
                
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
            format='%(asctime)s-%(process)d-pid.py  -%(levelname)s-%(message)s')
        
        logging.info("running BrewfermPID module tests")
        logging.info("finished BrewfermPID module tests")

    except Exception as e:
        logging.exception("%s %s", type(e), e)
