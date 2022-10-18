#!/usr/bin/env python
from bluepy import btle

# notes about bluetooth
# sudo pip3 install bluepy
# sudo hciconfig hci0 up
# use bluetoothctl program to turn 'scan on'

# Import standard libraries ---------------------------------------------------
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
logger = BrewfermLogger('blues.py').getLogger()


# Classes ------------------------------------------------------------
class BrewfermBlues:
    def __init__(self):
        self.sleep_time = 20  # in seconds
        self.uuid = None
        self.temp = None
        self.sg = None
        self.beacon_found = False

        self.xd = XchgData(paths.blue_out)

    def update(self):
        scanner = btle.Scanner()

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
        try:
            sg = str(int(self.sg, 16))
        except TypeError:
            if self.beacon_found:
                logger.warning('no tilt found')

            self.beacon_found = False
        else:
            if not self.beacon_found:
                logger.info('tilt found')

            self.beacon_found = True
            if int(self.sg, 16) >= 1000:
                readings['sg'] = '1.' + sg[1:4]
            else:
                readings['sg'] = '0.' + sg[1:4]

            readings['sgr'] = int(self.sg, 16)
            readings['temp'] = int(self.temp, 16)

            self.xd.write_blue(readings)


if __name__ == "__main__":
    try:
        logger.info("blues starting up")
        myblues = BrewfermBlues()

        killer = killer.GracefulKiller()
        not_ready = False

        while not killer.kill_now:
            try:
                myblues.update()
                myblues.implement_current()
                if not_ready:
                    logger.info('bluetooth ready')
                    not_ready = False

            except btle.BTLEManagementError:
                not_ready = True
                logger.warning('bluetooth not ready')

            sleep(myblues.sleep_time)

    except Exception as e:
        logger.exception("%s %s", type(e), e)

sleep(10)
logger.info('clean exit')
sys.exit(0)
