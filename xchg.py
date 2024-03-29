#!/usr/bin/python3

import json
import mmap
import sys

from datetime import datetime, timedelta
from pathlib import Path

import paths
from logger import BrewfermLogger


"""
Creates a rotating log
"""
logger = BrewfermLogger('xchg.py').getLogger()


# --------------------------------------------------------------------
# This class and it's get method used to communicate between processes
# --------------------------------------------------------------------
class XchgData():

    def __init__(self, path=None):
        self.path = path
        self.read_mode = 'r'
        self.update_mode = 'w'

        self.controller_mode = self.read_mode
        self.gui_mode = self.read_mode
        self.sensors_mode = self.read_mode
        self.relays_mode = self.read_mode
        self.blue_mode = self.read_mode

        if path is not None:
            if self.path == paths.sensors_out:
                self.sensors_mode = self.update_mode

            if self.path == paths.controller_out:
                self.controller_mode = self.update_mode

            if self.path == paths.relays_out:
                self.relays_mode = self.update_mode

            if self.path == paths.gui_out:
                self.gui_mode = self.update_mode

            if self.path == paths.blue_out:
                self.blue_mode = self.update_mode

        self.sensors_out = None
        self.controller_out = None
        self.relays_out = None
        self.blue_out = None
        self.gui_out = Xchg(paths.gui_out, self.gui_mode)

    def get(self, field_name, default=None):
        try:
            switcher = {
                paths.current: lambda: self.get_relays(field_name),
                paths.relays_ts: lambda: self.get_relays('ts'),

                paths.desired: lambda: self.get_controller(field_name),
                paths.desired_ts: lambda: self.get_controller('ts'),

                paths.chamber_temp: lambda: self.get_temp('chamber'),
                paths.beer_temp: lambda: self.get_temp('beer'),
                paths.ambient_temp: lambda: self.get_temp('ambient'),

                paths.beer_target: lambda: self.get_gui('beer_target'),
                paths.beerPID: lambda: self.get_gui('beer_pid'),
                paths.chamberPID: lambda: self.get_gui('chamber_pid'),
                paths.state: lambda: self.get_gui('state'),
                paths.sensor_map: lambda: self.get_gui('id_map'),
                paths.calibrations: lambda: self.get_gui('calibrations'),

                paths.sensors_raw: lambda: self.get_sensors_raw(),

                paths.blue_sg: lambda: self.get_blue(),
                paths.blue_ts: lambda: self.get_blue_ts(),

                paths.ambient_temp_offset: lambda: self.get_offset(field_name),
                paths.beer_temp_offset: lambda: self.get_offset(field_name),
                paths.chamber_temp_offset: lambda: self.get_offset(field_name)
            }

            result = switcher.get(field_name)  # returns a function object
            if result:
                x = result()
                if x is None:
                    # logger.debug('xchg get defaulting field %s', field_name)
                    # logger.debug('lambda result = %s', result())
                    return default
                else:
                    return result()  # execute the lambda expression function
            else:
                return default
        except Exception as e:
            logger.exception('%s %s', type(e), e)

    def get_offset(self, field_name):
        result = 0.0

        calibrations = self.get(paths.calibrations, {})
        map = self.get(paths.sensor_map, {})

        if field_name == paths.beer_temp_offset:
            role = 'beer'
        else:
            if field_name == paths.chamber_temp_offset:
                role = 'chamber'
            else:
                if field_name == paths.ambient_temp_offset:
                    role = 'ambient'

        for x in map:
            if map[x] == role:
                if x in calibrations:
                    result = calibrations[x]
                else:
                    result = 0.0

        return result

    def get_blue(self):
        try:
            if self.blue_out is None:
                self.blue_out = Xchg(paths.blue_out, self.blue_mode)

            x = self.blue_out.read()
            result = None
            if 'sg' in x.keys():
                result = x['sg']
        except Exception as e:
            logger.exception('%s %s', type(e), e)

        return result

    def get_blue_ts(self):
        try:
            if self.blue_out is None:
                self.blue_out = Xchg(paths.blue_out, self.blue_mode)

            x = self.blue_out.read()
            result = None
            if 'ts' in x.keys():
                result = x['ts']
        except Exception as e:
            logger.exception('%s %s', type(e), e)

        return result

    def get_relays(self, field_name):
        try:
            if self.relays_out is None:
                self.relays_out = Xchg(paths.relays_out, self.relays_mode)

            x = self.relays_out.read()

            result = None
            if field_name in x.keys():
                result = x[field_name]
        except Exception as e:
            logger.exception("%s %s", type(e), e)

        return result

    def get_gui(self, field_name):
        result = None

        try:
            if self.gui_out is None:
                self.gui_out = Xchg(paths.gui_out, self.gui_mode)

            x = self.gui_out.read()
            if x is None:
                x = {}

            if field_name in x.keys():
                result = x[field_name]
        except Exception as e:
            logger.exception("%s %s", type(e), e)
            return None
        else:
            return result

    def get_controller(self, field_name):
        result = None
        try:
            if self.controller_out is None:
                self.controller_out = Xchg(
                    paths.controller_out,
                    self.controller_mode)

            x = self.controller_out.read()
            if x:
                if field_name in x.keys():
                    result = x[field_name]
        except Exception as e:
            logger.exception("%s %s", type(e), e)

        return result

    def get_temp(self, usage):
        result = None
        try:
            id_map = self.get_gui('id_map')
            readings = self.get_sensors_raw()

            for sensor in id_map.keys():
                if id_map[sensor] == usage:
                    # logger.debug('id_map=%s sensor=%s readings=%s', id_map, sensor, readings)
                    result = readings[sensor]
        except Exception:  # as e:
            logger.debug('sensor=%s readings=%s', sensor, readings)
            # logger.exception('%s %s', type(e), e)
            return None
        else:
            return result

    def get_sensors_raw(self):
        try:
            if self.sensors_out is None:
                self.sensors_out = Xchg(paths.sensors_out, self.sensors_mode)

            result = self.sensors_out.read()
        except Exception as e:
            logger.exception("%s %s", type(e), e)

        return result

    def get_sensors(self, field_name):
        try:
            if self.sensors_out is None:
                self.sensors_out = Xchg(paths.sensors_out, self.sensors_mode)

            x = self.sensors_out.read()

            result = None
            if field_name in x.keys():
                result = x[field_name]
        except Exception as e:
            logger.exception("%s %s", type(e), e)

        return result

    def write_controller(self, value):
        try:
            if self.controller_mode != self.update_mode:
                logger.debug(
                    'attempted write to a file that opened ready only')
            else:
                if self.controller_out is None:
                    self.controller_out = Xchg(
                        paths.controller_out,
                        self.controller_mode)

                self.controller_out.write(value)
        except Exception as e:
            logger.exception("%s %s", type(e), e)

    def write_gui(self, value):
        try:
            if self.gui_mode != self.update_mode:
                logger.debug(
                    'attempted write to a file that opened ready only')
            else:
                if self.gui_out is None:
                    self.gui_out = Xchg(paths.gui_out, self.gui_mode)

                self.gui_out.write(value)
        except Exception as e:
            logger.exception("%s %s", type(e), e)

    def write_sensors(self, value):
        try:
            if self.sensors_mode != self.update_mode:
                logger.debug(
                    'attempted write to a file that opened ready only')
            else:
                if self.sensors_out is None:
                    self.sensors_out = Xchg(
                        paths.sensors_out,
                        self.sensors_mode)

                self.sensors_out.write(value)
        except Exception as e:
            logger.exception("%s %s", type(e), e)

    def write_relays(self, value):
        try:
            if self.relays_mode != self.update_mode:
                logger.debug(
                    'attempted write to a file that opened ready only')
            else:
                if self.relays_out is None:
                    self.relays_out = Xchg(paths.relays_out, self.relays_mode)

                self.relays_out.write(value)
        except Exception as e:
            logger.exception("%s %s", type(e), e)

    def write_blue(self, value):
        try:
            if self.blue_mode != self.update_mode:
                logger.debug(
                    'attempted write to a file that opened ready only')
            else:
                if self.blue_out is None:
                    self.blue_out = Xchg(paths.blue_out, self.blue_mode)

                self.blue_out.write(value)
        except Exception as e:
            logger.exception("%s %s", type(e), e)


# -------------------------------------------------------
# used internally
# -------------------------------------------------------
class Xchg():
    def __init__(self, path=None, mode='r', default={}):
        self.path = path
        self.mode = mode
        self.default = default  # should be a dict
        self.last = default
        self.pad = 1024
        self.mmap_file = None
        self.mm = None
        self.last_warning_ts = datetime.now() - timedelta(minutes=20)

        if mode == 'w':
            self.create()

    def create(self):
        try:
            current_size = Path(self.path).stat().st_size
        except FileNotFoundError:
            current_size = 0
        except Exception as e:
            logger.exception('in create %s %s', type(e), e)

        try:
            if current_size != self.pad:
                with open(self.path, 'wb') as f:
                    f.truncate()
                    f.flush()

                    self.default['ts'] = datetime.now().isoformat(
                        sep=' ',
                        timespec='seconds')

                    x = json.dumps(self.default)
                    y = x.ljust(self.pad, ' ')
                    f.write(y.encode('utf-8'))
                    f.close()
        except Exception as e:
            logger.exception("mmap file create %s %s", type(e), e)

    def read(self):
        try:

            if self.mmap_file is None:
                self.mmap_file = open(self.path, "r+")
                self.mm = mmap.mmap(self.mmap_file.fileno(), 0)

            self.mm.flush()
            self.mm.seek(0)
            s = self.mm.readline()
            self.last = json.loads(s.decode('utf-8'))

            return self.last
        except ValueError:
            if self.last_warning_ts < (datetime.now() - timedelta(minutes=5)):
                self.last_warning_ts = datetime.now()
                logger.warning("empty mmap file '%s'", self.path)
            return {}
        except FileNotFoundError:
            if self.last_warning_ts < (datetime.now() - timedelta(minutes=5)):
                self.last_warning_ts = datetime.now()
                logger.info('mmap file %s not available yet', self.path)
            return {}
        except Exception as e:
            logger.exception("mmap file read %s %s", type(e), e)
            sys.exit(1)

# expects a dictionary object in info
    def write(self, info=None):
        if self.mode == 'r':
            logger.exception('attempted write to Xchg opened as read')
        try:
            info['ts'] = datetime.now().isoformat(sep=' ', timespec='seconds')

            if self.mmap_file is None:
                self.mmap_file = open(self.path, 'r+')
                self.mm = mmap.mmap(self.mmap_file.fileno(), 0)

            self.mm.seek(0)

            j = json.dumps(info).ljust(self.pad).encode('utf-8')

            self.mm[0:len(j)] = j
            self.mm.flush()

        except Exception as e:
            logger.exception("mmap write %s %s", type(e), e)
            raise e


# module test runs if module invoked directly
if __name__ == '__main__':
    try:
        print('module test results in xchg.log')
        logger.info("controller starting up")

        a = {"module": "test"}
        x = Xchg('./module-test.mmap', mode='w', default=a)
        y = Xchg('./module-test.mmap', mode='r', default={"module": "fail"})

        b = None
        b = y.read()
        if a == b:
            logger.info('test passed..')
        else:
            logger.exception("a = '%s' but b = '%s'", a, b)

        a = None
        b = None
        a = {"module": "test2"}
        x.write(a)
        b = y.read()
        if a == b:
            logger.info('test2 passed..')
            logger.info('module tests successful')
        else:
            logger.exception(" a = '%s' but b = '%s'", a, b)

    except Exception as e:
        logger.exception("%s %s", type(e), e)
