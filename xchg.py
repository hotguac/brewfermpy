#!/usr/bin/python3

import json
import logging
import mmap

from datetime import datetime
from time import sleep

class Xchg():
    def __init__(self, path=None, mode='r', default=None):
        super().__init__()
        self.path = path
        self.mode = mode
        self.default = default # should be a dict
        self.last = default
        if mode == 'w':
            self.create()

    def create(self):
        try:
            with open(self.path, 'wb') as f:
                f.truncate()
                f.flush()
                f.write(json.dumps(self.default).encode('utf-8'))
                f.close()
        except Exception as e:
            logging.exception("mmap file create %s %s", type(e), e)
        
    def read(self):
        try:
            with open(self.path,"r+") as f:
                mm = mmap.mmap(f.fileno(), 0)
                mm.seek(0)
                self.last = json.loads(mm.readline().decode('utf-8'))
                mm.flush()
                mm.close()
                return self.last
        except ValueError as e:
            logging.warning("empty mmap file '%s'", self.path)
            self.last = None
            return self.default
        except Exception as e:            
            logging.exception("mmap file read %s %s", type(e), e)
            self.last = None
            return self.default

    def write(self, info=None):
        if self.mode == 'r':
            logging.exception('attempted write to Xchg opened as read')
        try:
            info['ts'] = datetime.now().isoformat(sep=' ', timespec='seconds')
            with open(self.path, 'wb') as f:
                f.truncate()
                f.flush()
                f.write(json.dumps(info).encode('utf-8'))
                f.close()
        except Exception as e:
            logging.exception("mmap file update %s %s", type(e), e)

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
