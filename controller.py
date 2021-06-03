import atexit
import logging
import math
import os
import signal
import sys

import inspect

from datetime import datetime
from time import sleep

# Import application libraries ------------------------------------------------
import brewdb
import paths

from pid import BeerPID
from pid import ChamberPID
from xchg import Xchg

class BrewfermController():
    def __init__(self):
        super().__init__()

        self.set_initial_state()
        self.setup_xchg()
        self.beerPID = BeerPID(64)
        self.chamberPID = ChamberPID(64)
        self.chamberPID.change_target(65)

        
    def update(self):
        self.get_relays()
        self.get_sensors()
        self.calculate()
        self.update_relays()
        self.update_gui()

    def get_relays(self):
        try:
            readings = self.relays_out.read()
            self.current_state = readings['current']

        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def get_sensors(self):
        try:
            readings = self.sensors_out.read()
            self.beer_temp = float(readings['sensor1'])
            self.chamber_temp = float(readings['sensor2'])
            self.ambient_temp = float(readings['sensor3'])
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def calculate(self):
        try:
            x = self.beerPID.update(self.beer_temp)
    
            self.chamberPID.change_target(x)
            self.heat_cool = self.chamberPID.update(float(self.chamber_temp))
            # logging.debug('chamber target = %s heat cool control = %s', x, self.heat_cool)
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def update_relays(self):
        try:
            x = 1
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def update_gui(self):
        try:
            self.gui_in.write(self.format_gui())
        except Exception as e:
            logging.exception("%s %s", type(e), e)


    def set_initial_state(self):
        self.beer_temp = 0.0
        self.beer_target = 64.0
        self.chamber_temp = 00.0

        self.desired_state = paths.idle
        self.current_state = paths.idle

    def format_gui(self):
        try:
            temp = {}
            temp[paths.beer_temp] = self.beer_temp
            temp[paths.beer_target] = self.beer_target
            temp[paths.chamber_temp] = self.chamber_temp
            temp[paths.current] = self.current_state
            temp[paths.desired] = self.desired_state
        except Exception as e:
            logging.exception('%s %s', type(e), e)

        return temp

    def setup_xchg(self):
        self.sensors_out = Xchg(paths.sensors_out)
        self.relays_out = Xchg(paths.relays_out)
        self.gui_out = Xchg(paths.gui_out)

        self.relays_in = Xchg(paths.relays_in, 'w')
        self.relays_in.write({paths.desired : paths.idle})

        self.gui_in = Xchg(paths.gui_in, 'w')
        self.gui_in.write(self.format_gui())

        
# main loop here
print('past class def')

if __name__ == '__main__':
    try:
        logging.basicConfig(
            level=logging.DEBUG, filename=paths.logs, 
            format='%(asctime)s-%(process)d-controller.py -%(levelname)s-%(message)s')

        logging.info("controller starting up")

        mycontroller = BrewfermController()
        
        logging.info("controller init complete")

        count = 0
        while count < 600:
            count = count + 1
            mycontroller.update()
            sleep(20)

    except Exception as e:
        logging.exception("%s %s", type(e), e)
