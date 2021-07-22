#!/usr/bin/python3

# Import standard libraries ---------------------------------------------------
import logging
import os
import random
import sys

from datetime import datetime
from time import sleep

# Import application libraries ------------------------------------------------
import killer
import paths
from xchg import XchgData


# Functions ------------------------------------------------------------
class BrewfermSensors:
    def __init__(self):
        self.xd = XchgData(paths.sensors_out)
        self.last_emulation = datetime.now()
        self.current_reading = {}
        self.sleep_time = 4  # seconds

        # degrees F per second empty chamber
        self.heat_rate = 12.0 / (60 * 60)
        self.cool_rate = 60.0 / (60 * 60)

        # degrees F per second per degree difference
        self.chamber_to_beer = 0.3 / (60 * 60)
        self.beer_to_chamber = 1.4 / (60 * 60)
        self.ambient_to_chamber = 0.05 / (60 * 60)

    def sleep_for(self):
        return self.sleep_time

    def update_mapping(self):
        try:
            self.id_map = self.xd.get('sensor_map', {})
        except Exception as e:
            logging.exception('update_mapping %s %s', type(e), e)

# TODO: Make all rates time based and use the time between calls
    def emulate_temps(self):
        ambient = 80  # degrees F

        beer = self.xd.get('beer', 64)
        chamber = self.xd.get('chamber', 64)
        current = self.xd.get('current', paths.idle)

        check_time = datetime.now()
        elapsed = check_time - self.last_emulation
        self.last_emulation = check_time

        elapsed_seconds = (
            (elapsed.days * 24 * 60 * 60)
            + elapsed.seconds
            + (elapsed.microseconds / 1000000)
        )

        if elapsed_seconds < (self.sleep_time * 3):
            if current == paths.heat:
                chamber += elapsed_seconds * self.heat_rate  # 0.01
            elif current == paths.cool:
                chamber -= elapsed_seconds * self.cool_rate  # 0.15

            beer += (chamber - beer) * (elapsed_seconds * self.chamber_to_beer)
            chamber += (
                (beer - chamber) * (elapsed_seconds * self.beer_to_chamber)
            )

            chamber += (
                (ambient - chamber)
                * (elapsed_seconds * self.ambient_to_chamber)
            )

        result = {}
        result['sensor1'] = beer
        result['sensor2'] = chamber
        result['sensor3'] = str(ambient + random.uniform(-0.2, 0.1))

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
                        #logging.info('found %s', candidate.name)
                        temp_f = (float(t1) * 9.0) / 5000 + 32.0
                        self.current_reading[candidate.name] = temp_f
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
                #logging.debug('line2=%s', line)
                mytemp = line.rsplit('t=', 1)[1]
            else:
                mytemp = None
                logging.error("CRC not valid for sensor id=%s", id)

            f.close()

            return mytemp
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
            sleep(mysensors.sleep_for())

    except Exception as e:
        logging.exception("Some other error %s %s", type(e), e)
        sys.exit(1)
    else:
        logging.info("clean exit")
        sys.exit(0)
