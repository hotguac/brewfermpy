#!/usr/bin/python3

# Import standard libraries ---------------------------------------------------
import atexit
import logging
import os
import random
import sys

from datetime import datetime
from time import sleep

# Import application libraries ------------------------------------------------
import paths
from xchg import Xchg

# Functions ------------------------------------------------------------

class BrewfermSensors:
    def __init__(self):
        self.xchg_out = Xchg(paths.sensors_out, mode='w', default={'sensor1':'00.0', 'sensor2':'00.0', 'sensor3':'00.0' })
        self.default_reading = {'sensor1':'00.0', 'sensor2':'00.0', 'sensor3':'00.0'}
        self.last_reading = {}
        self.current_reading = {}

    def random_temps(self):
        result = {}
        result['sensor1'] = str(64.3 + random.uniform(-0.5, 0.5))
        result['sensor2'] = str(64.2 + random.uniform(-0.7, 0.7))
        result['sensor3'] = str(69.5 + random.uniform(-2.0, 2.0))
        
        return result

    def write_temps(self):
        self.scan_sensors()
        if self.current_reading:
            self.xchg_out.write(self.current_reading)
        else:
            self.xchg_out.write(self.random_temps())

    def scan_sensors(self):
        self.current_reading = {}

        try:
            with os.scandir('/sys/bus/w1/devices/') as possible:
                for candidate in possible:
                    t1 = self.gettemp(candidate.name)
                    if t1 is not None:
                        logging.info('found %s', candidate.name)                    
                        self.current_reading[candidate.name] = t1
        except Exception as e:
            logging.exception('scan_sensors')

    def gettemp(self, id):
        try:
            mytemp = ''
            filename = 'w1_slave'
            
            f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
            line = f.readline() # read 1st line
            
            crc = line.rsplit(' ',1)
            crc = crc[1].replace('\n', '')
            
            if crc == 'YES':
                line = f.readline() # read 2nd line
                mytemp = float(line.rsplit('t=',1))
            else:
                mytemp = float(-99999)
                logging.error("CRC not valid for sensor id=%s",id)
                
            f.close()
        
            return int(mytemp[1])
        except FileNotFoundError as e:
            # not everything in the directory is a one-wire temp sensor
            return None
        except Exception as e:
            logging.exception("reading one-wire interface for sensor id=%s : %s", id, e)
            return None

# Run Loop Here --------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename=paths.logs, 
                        format='%(asctime)s-%(process)d-sensors.py -%(levelname)s-%(message)s')

    logging.info("sensors starting up")
    try:
        mysensors = BrewfermSensors()

        count = 0
        while (count < 600):
            count = count + 1

            mysensors.write_temps()
            sleep(8)

    except Exception as e:
        logging.exception("Some other error %s %s", type(e), e)
        sys.exit(1)
    else:
        logging.info("clean exit")
        sys.exit(1)
       