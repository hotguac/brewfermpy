#!/usr/bin/python3

# Import standard libraries ---------------------------------------------------
import atexit
import logging
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

def gettemp():
    #logging.debug("in gettemp()")
    return (0.0)

def format_temps():
    sr = {'ts':datetime.now().isoformat(sep=' ', timespec='seconds'), 'sensor1':'00.0', 'sensor2':'00.0', 'sensor3':'00.0' }   
    return json.dumps(sr).encode('utf-8')

# Run Loop Here --------------------------------------------------------
logging.basicConfig(level=logging.DEBUG, filename=paths.logs, format='%(asctime)s-%(process)d-sensors.py -%(levelname)s-%(message)s')
logging.debug("sensors starting up")

if __name__ == '__main__':
    try:
#        xchg_out = Xchg('/home/pi/brewferm/xchg/sensors_out.mmap',mode='w',default={'sensor1':'00.0', 'sensor2':'00.0', 'sensor3':'00.0' })
        xchg_out = Xchg(paths.sensors_out, mode='w', default={'sensor1':'00.0', 'sensor2':'00.0', 'sensor3':'00.0' })

        count = 0
        while (count < 1200):
            count = count + 1

            tmp = gettemp()
            if tmp == None:
                logging.warning("Sensor not attached")

            xchg_out.write({'sensor1':'00.1', 'sensor2':'00.1', 'sensor3':'00.1' })    
            #update_mmap(63.9+(float(count)/150.1), 65.7-(float(count)/160.1))
            sleep(600)

    except Exception as e:
        logging.exception("Some other error %s %s", type(e), e)
        sys.exit(1)
    else:
        logging.debug("clean exit")
        sys.exit(1)