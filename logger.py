#!/usr/bin/python3

# Import standard libraries ---------------------------------------------------
import logging
from logging.handlers import TimedRotatingFileHandler
import paths


# Classes ------------------------------------------------------------
class BrewfermLogger:
    def __init__(self, module):
        self.logger = logging.getLogger("Brewferm")

        # loggers are a singleton, don't reconfigure if already created
        if not len(self.logger.handlers):
            self.logger.setLevel(logging.DEBUG)
            # add a rotating handler
            handler = TimedRotatingFileHandler(
                paths.logs,
                when="h",
                interval=12,
                backupCount=15
                )

            # create formatter
            formatter = logging.Formatter('%(asctime)s-%(process)d-%(filename)s-%(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            self.logger.addHandler(handler)

    def getLogger(self):
        return self.logger
