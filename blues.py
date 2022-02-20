#!/usr/bin/env python
from bluepy import btle

# notes about bluetooth
# sudo pip3 install bluepy
# sudo hciconfig hci0 up
# use bluetoothctl program to turn 'scan on'

# Import standard libraries ---------------------------------------------------
import logging
import sys

from time import sleep

# Import application libraries ------------------------------------------------
import killer
import paths
from xchg import XchgData


# Classes ------------------------------------------------------------
class BrewfermBlues:
    def __init__(self):
        self.sleep_time = 120  # in seconds
        self.uuid = None
        self.temp = None
        self.sg = None

        self.xd = XchgData(paths.blue_out)

    def update(self):
        scanner = btle.Scanner()

        # logging.debug('Scanning for devices...')
        devices = scanner.scan(4)  # timeout in seconds

        for d in devices:
            for (sdid, desc, val) in d.getScanData():
                if sdid == 255:
                    if val[:6] == '4c0002':
                        self.uuid = val[8:40]
                        self.temp = val[40:44]
                        self.sg = val[44:48]

    def implement_current(self):
        readings = {}
        sg = str(int(self.sg, 16))
        if int(self.sg, 16) >= 1000:
            readings['sg'] = '1.' + sg[1:4]
        else:
            readings['sg'] = '0.' + sg[1:4]

        readings['sgr'] = int(self.sg, 16)
        readings['temp'] = int(self.temp, 16)

        self.xd.write_blue(readings)


if __name__ == "__main__":
    try:
        logging.basicConfig(
            level=logging.DEBUG, filename=paths.logs,
            format=(
                '%(asctime)s-%(process)d-blue.py  '
                '-%(levelname)s-%(message)s'))

        logging.info("blues starting up")
        myblues = BrewfermBlues()

        killer = killer.GracefulKiller()
        while not killer.kill_now:
            myblues.update()
            myblues.implement_current()
            sleep(myblues.sleep_time)

    except Exception as e:
        logging.exception("%s %s", type(e), e)

sleep(10)
logging.info('clean exit')
sys.exit(0)
