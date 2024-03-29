#!/usr/bin/python3

# Import standard libraries ---------------------------------------------------
import os
import sys
from time import sleep

# Import application libraries ------------------------------------------------
import killer
import paths
from xchg import XchgData
from logger import BrewfermLogger


"""
Creates a rotating log
"""
logger = BrewfermLogger('sensors.py').getLogger()


# Functions ------------------------------------------------------------
class BrewfermSensors:
    def __init__(self):
        self.xd = XchgData(paths.sensors_out)
        self.current_reading = {}
        self.sleep_time = 4  # seconds
        self.read_good = True

    def sleep_for(self):
        return self.sleep_time

    def write_temps(self):
        self.scan_sensors()
        if self.current_reading:
            self.xd.write_sensors(self.current_reading)
            if not self.read_good:
                logger.info('sensors read')
                self.read_good = True
        else:
            if self.read_good:
                logger.warning('no sensors read')
                self.read_good = False

    def scan_sensors(self):
        self.current_reading = {}

        try:
            with os.scandir('/sys/bus/w1/devices/') as possible:
                for candidate in possible:
                    t1 = self.gettemp(candidate.name)
                    if t1 is not None:
                        temp_f = (float(t1) * 9.0) / 5000 + 32.0
                        self.current_reading[candidate.name] = temp_f
        except Exception as e:
            logger.exception('%s %s', type(e), e)

    def gettemp(self, id):
        try:
            mytemp = ''
            filename = 'w1_slave'

            f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
            line = f.readline()  # read 1st line

            crc = line.rsplit(' ', 1)
            crc = crc[1].replace('\n', '')

            if crc == 'YES':
                line = f.readline()  # read 2nd line
                mytemp = line.rsplit('t=', 1)[1]
            else:
                mytemp = None
                logger.error("CRC not valid for sensor id=%s", id)

            f.close()

            return mytemp
        except FileNotFoundError:
            # not everything in the directory is a one-wire temp sensor
            return None
        except IndexError:
            return None
        except Exception as e:
            logger.exception(
                'reading one-wire interface for sensor id=%s : %s',
                id,
                e)
            return None

# Run Loop Here --------------------------------------------------------


if __name__ == '__main__':
    logger.info("sensors starting up")
    try:
        mysensors = BrewfermSensors()

        killer = killer.GracefulKiller()
        while not killer.kill_now:
            # mysensors.update_mapping()
            mysensors.write_temps()
            sleep(mysensors.sleep_for())

    except Exception as e:
        logger.exception("Some other error %s %s", type(e), e)
        sys.exit(1)
    else:
        logger.info("clean exit")
        sys.exit(0)
