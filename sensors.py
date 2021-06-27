#!/usr/bin/python3

# Import standard libraries ---------------------------------------------------
import logging
import os
import random
import sys

from time import sleep

# Import application libraries ------------------------------------------------
import killer
import paths
from xchg import XchgData


# Functions ------------------------------------------------------------
class BrewfermSensors:
    def __init__(self):
        self.xd = XchgData(paths.sensors_out)

        self.current_reading = {}

    def update_mapping(self):
        try:
            self.id_map = self.xd.get('sensor_map', {})
        except Exception as e:
            logging.exception('update_mapping %s %s', type(e), e)

    def emulate_temps(self):
        beer = self.xd.get('beer', 64)
        chamber = self.xd.get('chamber', 64)
        current = self.xd.get('current', paths.idle)

        if current == paths.heat:
            chamber += 0.03
        elif current == paths.cool:
            chamber -= 0.15

        beer = ((beer * 99) + chamber) / 100  # transfer from chamber to beer
        chamber = ((chamber * 59) + beer) / 60  # transfer from beer to chamber

        result = {}
        result['sensor1'] = beer
        result['sensor2'] = chamber
        result['sensor3'] = str(89.5 + random.uniform(-0.6, 0.6))

        return result

    def map_sensors(self, readings):
        result = {}
        count = 0
        try:
            for id in readings.keys():
                if id in self.id_map:
                    result[self.id_map[id]] = {id: readings[id]}
                else:
                    count += 1
                    result['unknown_' + str(count)] = {id: readings[id]}
        except Exception as e:
            logging.exception('map_sensors %s %s', type(e), e)

        return result

    def write_temps(self):
        self.scan_sensors()
        if self.current_reading:
            self.xd.write_sensors(self.map_sensors(self.current_reading))
        else:
            self.xd.write_sensors(self.map_sensors(self.emulate_temps()))

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
            logging.exception('%s %s', type(e), e)

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
                mytemp = float(line.rsplit('t=', 1))
            else:
                mytemp = float(-99999)
                logging.error("CRC not valid for sensor id=%s", id)

            f.close()

            return int(mytemp[1])
        except FileNotFoundError:
            # not everything in the directory is a one-wire temp sensor
            return None
        except Exception as e:
            logging.exception(
                'reading one-wire interface for sensor id=%s : %s',
                id,
                e)
            return None

# Run Loop Here --------------------------------------------------------


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, filename=paths.logs,
        format='%(asctime)s-%(process)d-sensors.py -%(levelname)s-%(message)s')

    logging.info("sensors starting up")
    try:
        mysensors = BrewfermSensors()

        killer = killer.GracefulKiller()
        while not killer.kill_now:
            mysensors.update_mapping()
            mysensors.write_temps()
            sleep(4)

    except Exception as e:
        logging.exception("Some other error %s %s", type(e), e)
        sys.exit(1)
    else:
        logging.info("clean exit")
        sys.exit(0)
