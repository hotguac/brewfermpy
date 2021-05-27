#!/usr/bin/python3

# Import standard libraries ---------------------------------------------------
import atexit
import logging
import random
import sys

from datetime import datetime
from time import sleep

# Import application libraries ------------------------------------------------
import paths
from xchg import Xchg

# Functions ------------------------------------------------------------

# def gettemp(id):
#     try:
#         mytemp = ''
#         filename = 'w1_slave'
        
#         f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
#         line = f.readline() # read 1st line
        
#         crc = line.rsplit(' ',1)
#         crc = crc[1].replace('\n', '')
        
#         if crc=='YES':
#             line = f.readline() # read 2nd line
#             mytemp = float(line.rsplit('t=',1))
#         else:
#             mytemp = float(-99999)
#             logging.error("CRC not valid for sensor id=%s",id)
            
#         f.close()
    
#         return int(mytemp[1])
#     except FileNotFoundError as e:
#         logging.error("sensor not found, id=%s : %s", id, e)
#         return None
#     except Exception as e:
#         logging.debug("%s", type(e))
#         logging.error("reading one-wire interface for sensor id=%s : %s", id, e)
#         return None

class BrewfermSensors:
    def __init__(self):
        self.xchg_out = Xchg(paths.sensors_out, mode='w', default={'sensor1':'00.0', 'sensor2':'00.0', 'sensor3':'00.0' })
        self.current_reading = {'sensor1':'00.0', 'sensor2':'00.0', 'sensor3':'00.0'}
        self.last_reading = {}

    def format_temps(self):
        result = {}
        result['sensor1'] = str(64.3 + random.uniform(-0.5,0.5))
        result['sensor2'] = str(64.2 + random.uniform(-0.7,0.7))
        result['sensor3'] = str(69.5 + random.uniform(-2.0,2.0))
        
        return result

        #return {'sensor1':'00.0', 'sensor2':'00.0', 'sensor3':'00.0' }   

    def write_temps(self):
        self.xchg_out.write(self.format_temps())

# Run Loop Here --------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename=paths.logs, format='%(asctime)s-%(process)d-sensors.py -%(levelname)s-%(message)s')
    logging.debug("sensors starting up")
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
        logging.debug("clean exit")
        sys.exit(1)
       