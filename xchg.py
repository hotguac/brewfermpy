#!/usr/bin/python3

import json
import logging
import mmap
import sys

from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

import paths

# ---------------------------------------------------------------------------------------------------------        
# 
# ---------------------------------------------------------------------------------------------------------        
class XchgData():
    def __init__(self, path=None):
        self.path = path
        self.read_mode = 'r'
        self.update_mode = 'w'

        self.controller_mode = self.read_mode
        self.gui_mode = self.read_mode
        self.sensors_mode = self.read_mode
        self.relays_mode = self.read_mode
        
        if path is not None:
            if self.path == paths.sensors_out:
                self.sensors_mode = self.update_mode

            if self.path == paths.controller_out:
                self.controller_mode = self.update_mode

            if self.path == paths.relays_out:
                self.relays_mode = self.update_mode

            if self.path == paths.gui_out:
                self.gui_mode = self.update_mode

        self.sensors_out = None
        self.controller_out = None
        self.relays_out = None
        self.gui_out = Xchg(paths.gui_out, self.gui_mode)

    def get_current_state(self):
        try:
            if self.relays_out is None:
                self.relays_out = Xchg(paths.relays_out, self.relays_mode)
                
            x = self.relays_out.read()

            if 'current' in x.keys():
                return x['current']
            else:
                return None
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def get_desired_state(self):
        try:
            if self.controller_out is None:
                self.controller_out = Xchg(paths.controller_out, self.controller_mode)
                
            x = self.controller_out.read()

            if 'desired' in x.keys():
                return x['desired']
            else:
                return None
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def get_desired_ts(self):
        try:
            if self.controller_out is None:
                self.controller_out = Xchg(paths.controller_out, self.controller_mode)
                
            x = self.controller_out.read()

            if 'ts' in x.keys():
                return x['ts']
            else:
                return None
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def get_chamber_temp(self):
        try:
            result = None
            if self.sensors_out is None:
                self.sensors_out = Xchg(paths.sensors_out, self.sensors_mode)
                
            x = self.sensors_out.read()
            if 'chamber' in x.keys():
                for ct in x['chamber'].keys():
                    result = float(x['chamber'][ct])
            return result
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def get_beer_temp(self):
        try:
            result = None
            if self.sensors_out is None:
                self.sensors_out = Xchg(paths.sensors_out, self.sensors_mode)
                
            x = self.sensors_out.read()
            if 'beer' in x.keys():
                for ct in x['beer'].keys():
                    result = float(x['beer'][ct])
            return result
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def get_target_temp(self):
        try:
            result = None
            if self.gui_out is None:
                self.gui_out = Xchg(paths.gui_out, self.gui_mode)
                
            x = self.gui_out.read()
            if 'beer_target' in x.keys():
                result = float(x['beer_target'])
                
            return result
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def get_sensor_map(self):
        try:
            result = {}
            if self.gui_out is None:
                self.gui_out = Xchg(paths.gui_out, self.gui_mode)
                
            x = self.gui_out.read()
            if 'id_map' in x.keys():
                result = x['id_map']
                
            return result
        except Exception as e:
            logging.exception("%s %s", type(e), e)


    def get_paused_state(self):
        try:
            result = None
            if self.gui_out is None:
                self.gui_out = Xchg(paths.gui_out, self.gui_mode)
                
            x = self.gui_out.read()
            if 'state' in x.keys():
                result = x['state']
                
            return result
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def write_controller(self, value):
        try:
            if self.controller_mode != self.update_mode:
                logging.debug('attempted write to a file that opened ready only')
            else:
                if self.controller_out is None:
                    self.controller_out = Xchg(paths.controller_out, self.controller_mode)

                self.controller_out.write(value)
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def write_gui(self, value):
        try:
            if self.gui_mode != self.update_mode:
                logging.debug('attempted write to a file that opened ready only')
            else:
                if self.gui_out is None:
                    self.gui_out = Xchg(paths.gui_out, self.gui_mode)

                self.gui_out.write(value)
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def write_sensors(self, value):
        try:
            if self.sensors_mode != self.update_mode:
                logging.debug('attempted write to a file that opened ready only')
            else:
                if self.sensors_out is None:
                    self.sensors_out = Xchg(paths.sensors_out, self.sensors_mode)

                self.sensors_out.write(value)
        except Exception as e:
            logging.exception("%s %s", type(e), e)

    def write_relays(self, value):
        try:
            if self.relays_mode != self.update_mode:
                logging.debug('attempted write to a file that opened ready only')
            else:
                if self.relays_out is None:
                    self.relays_out = Xchg(paths.relays_out, self.relays_mode)

                self.relays_out.write(value)
        except Exception as e:
            logging.exception("%s %s", type(e), e)

# ---------------------------------------------------------------------------------------------------------        
# 
# ---------------------------------------------------------------------------------------------------------        
class Xchg():
    def __init__(self, path=None, mode='r', default={}):
        #super().__init__()
        self.path = path
        self.mode = mode
        self.default = default # should be a dict
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
        except FileNotFoundError as e:
            current_size = 0
        except Exception as e:
            logging.exception('in create %s %s', type(e), e)
            
        try:            
            if current_size != self.pad:
                with open(self.path, 'wb') as f:
                    f.truncate()
                    f.flush()

                    self.default['ts'] = datetime.now().isoformat(sep=' ', timespec='seconds')
                    x = json.dumps(self.default)
                    y = x.ljust(self.pad, ' ')
                    f.write(y.encode('utf-8'))
                    f.close()
        except Exception as e:
            logging.exception("mmap file create %s %s", type(e), e)
        
    def read(self):
        try:
            
            if self.mmap_file is None:
                self.mmap_file = open(self.path,"r+")
                self.mm = mmap.mmap(self.mmap_file.fileno(), 0)

            self.mm.seek(0)
            s = self.mm.readline()
            self.last = json.loads(s.decode('utf-8'))
            return self.last
        except ValueError as e:
            if self.last_warning_ts < (datetime.now() - timedelta(minutes=5)):
                self.last_warning_ts = datetime.now()
                logging.warning("empty mmap file '%s'", self.path)
            return {}
        except FileNotFoundError as e:
            if self.last_warning_ts < (datetime.now() - timedelta(minutes=5)):
                self.last_warning_ts = datetime.now()
                logging.warning('mmap file %s not found', self.path)
            return {}
        except Exception as e:            
            logging.exception("mmap file read %s %s", type(e), e)
            sys.exit(1)

# expects a dictionary object in info
    def write(self, info=None):
        if self.mode == 'r':
            logging.exception('attempted write to Xchg opened as read')
        try:
            info['ts'] = datetime.now().isoformat(sep=' ', timespec='seconds')

            if self.mmap_file is None:
                self.mmap_file = open(self.path,'r+') # "wb")
                self.mm = mmap.mmap(self.mmap_file.fileno(), 0)

            self.mm.seek(0)

            j = json.dumps(info).ljust(self.pad).encode('utf-8')

            self.mm[0:len(j)] = j
            self.mm.flush()          

        except Exception as e:
            logging.exception("mmap write %s %s", type(e), e)
            raise(e)

# module test runs if module invoked directly
if __name__ == '__main__':
    try:
        print('module test results in xchg.log')
        logging.basicConfig(level=logging.DEBUG, filename='./xchg.log',format='%(asctime)s-%(process)d-xchg.py -%(levelname)s-%(message)s')
        logging.debug("controller starting up")


        a = {"module":"test"}
        x = Xchg('./module-test.mmap', mode='w', default=a)
        y = Xchg('./module-test.mmap', mode='r', default={"module":"fail"})
        
        b = None
        b = y.read()
        if a == b:
            logging.info('test passed..')
        else:
            logging.exception("a = '%s' but b = '%s'", a, b)

        a = None
        b = None
        a = {"module":"test2"}
        x.write(a)
        b = y.read()
        if a == b:
            logging.info('test2 passed..')
            logging.info('module tests successful')
        else:
            logging.exception(" a = '%s' but b = '%s'", a, b)
        
    except Exception as e:
        logging.exception("%s %s", type(e), e)
