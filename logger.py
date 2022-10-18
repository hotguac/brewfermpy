#!/usr/bin/python3

# Import standard libraries ---------------------------------------------------
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import WatchedFileHandler
import paths


# Classes ------------------------------------------------------------
class BrewfermLogger:
    def __init__(self, module):
        self.logger = logging.getLogger("Brewferm")

        # loggers are a singleton, don't reconfigure if already created
        if not len(self.logger.handlers):
            
            self.logger.setLevel(logging.DEBUG)

            if module == 'webs.py':
                log = logging.getLogger('werkzeug')
                log.setLevel(logging.ERROR)

            if module == 'controller.py':
                handler = RotatingFileHandler(
                    paths.logs,
                    maxBytes=24000,
                    backupCount=12
                    )
            else:
                handler = WatchedFileHandler(paths.logs)

            formatter = logging.Formatter('%(asctime)s-%(process)d-%(filename)s-%(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            self.logger.addHandler(handler)

    def getLogger(self):
        return self.logger
