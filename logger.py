#!/usr/bin/python3

# Import standard libraries ---------------------------------------------------
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import WatchedFileHandler
import paths


# Classes ------------------------------------------------------------
class BrewfermLogger:
    def __init__(self, module):
        self.logger = logging.getLogger("Brewferm")

        # loggers are a singleton, don't reconfigure if already created
        if not len(self.logger.handlers):
            self.logger.setLevel(logging.DEBUG)
            x = None
            # add a rotating handler
            if module == 'controller.py':
                handler = TimedRotatingFileHandler(
                    paths.logs,
                    when="h",
                    interval=12,
                    backupCount=15
                    )
                x = 'using timed rotating log'
            else:
                handler = WatchedFileHandler(paths.logs)
                x = 'using watched file log'

            # create formatter
            formatter = logging.Formatter('%(asctime)s-%(process)d-%(filename)s-%(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            self.logger.addHandler(handler)
            self.logger.info('%s for module %s', x, module)
        else:
            self.logger.info('singleton found for module %s', module)

    def getLogger(self):
        return self.logger
