import atexit
import logging
import math
import os
import sys

import inspect

from datetime import datetime
from time import sleep

# Import application libraries ------------------------------------------------
import brewdb
import killer
import paths

from pid import BeerPID
from pid import ChamberPID
from xchg import Xchg, XchgData

# ---------------------------------------------------------------------------------------------------------        
# 
# ---------------------------------------------------------------------------------------------------------        
class BrewfermController():
    def __init__(self):
        super().__init__()

        self.xd = XchgData(paths.controller_out)
        self.beer_temp = self.xd.get_beer_temp()
        self.chamber_temp = self.xd.get_chamber_temp()
        self.beer_target = self.xd.get_target_temp()
        self.current_state = self.xd.get_current_state()
        self.desired_state = paths.idle

        self.beerPID = BeerPID(self.beer_target)
        self.chamberPID = ChamberPID(self.beer_target)
        
        self.beerPID_tuning = {'empty' : 'yes'}
        self.chamberPID_tuning = {'empty' : 'yes'}

    def update(self):
        self.beer_temp = self.xd.get_beer_temp()
        self.chamber_temp = self.xd.get_chamber_temp()
        self.beer_target = self.xd.get_target_temp()
        self.current_state = self.xd.get_current_state()

        if self.xd.get_paused_state() == paths.paused:
            self.desired_state = paths.paused
        else:
            self.calculate()
            self.desired_state = paths.idle

            if self.heat_cool > 60:
                self.desired_state = paths.heat
            if self.heat_cool < 40:
                self.desired_state = paths.cool

        self.output_desired()
        self.beerPID_tuning = self.beerPID.get_tuning()
        self.chamberPID_tuning = self.chamberPID.get_tuning()
        
    def calculate(self):
        try:
            x = self.beerPID.update(self.beer_temp)
    
            self.chamberPID.change_target(x)
            self.heat_cool = self.chamberPID.update(float(self.chamber_temp))
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def output_desired(self):
        try:
            self.xd.write_controller({paths.desired : self.desired_state})
        except Exception as e:
            logging.exception("%s %s", type(e), e)

# ---------------------------------------------------------------------------------------------------------        
# main loop here
# ---------------------------------------------------------------------------------------------------------        
if __name__ == '__main__':
    try:
        logging.basicConfig(
            level=logging.DEBUG, filename=paths.logs, 
            format='%(asctime)s-%(process)d-controller.py -%(levelname)s-%(message)s')

        logging.info("controller starting up")

        mycontroller = BrewfermController()
        
        killer = killer.GracefulKiller()

        while not killer.kill_now:
            mycontroller.update()
            sleep(2)

        logging.info('shutting down')
        sys.exit(0)

    except Exception as e:
        logging.exception("%s %s", type(e), e)
