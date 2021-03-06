#!/usr/bin/python3

# Import 3rd party libraries --------------------------------------------------
import tkinter as tk
import tkinter.font as tkFont

# Import standard libraries ---------------------------------------------------
import os
import signal
import sys

# Import application libraries ------------------------------------------------
import colors

from gui_top import gTop
from gui_middle import gMiddle
from gui_bottom import gBottom

from logger import BrewfermLogger


"""
Creates a rotating log
"""
logger = BrewfermLogger('gui.py').getLogger()


# Functions -------------------------------------------------------------------
# make sure there is an environment variable for DISPLAY
# so we can run the GUI
def check_display():
    if os.environ.get('DISPLAY', '') == '':
        logger.warning('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')


def closing_time(self, *args):
    logger.info("shutting down")
    if tg is not None:
        tg.quit()
    if gm is not None:
        gm.quit()
    if bg is not None:
        bg.quit()
    if root is not None:
        root.quit()
    sys.exit(0)


# App -------------------------------------------------------------------------
logger.info("gui starting up")

try:
    check_display()

    root = tk.Tk()
    signal.signal(signal.SIGTERM, closing_time)

    root.attributes("-fullscreen", True)
    root.configure(bg=colors.background)
    root.configure(cursor="none")

    root.update_idletasks()
except tk.TclError:
    logger.info("exiting, display not ready yet...")
    sys.exit(0)
except Exception as e:
    logger.exception("%s %s", type(e), e)
    sys.exit(1)
else:
    logger.info(
        "Canvas Size = height %d and width %d",
        root.winfo_height(),
        root.winfo_width())
    logger.info('Available fonts=%s', tkFont.names())

#
#   Widgets -----------------------------------
#
try:
    tg = gTop(master=root)
    gm = gMiddle(master=root)
    bg = gBottom(master=root)
except Exception as e:
    logger.exception("%s %s", type(e), e)

#
#   Display -----------------------------------
#
try:
    root.mainloop()
except Exception as e:
    logger.exception("%s %s", type(e), e)

sys.exit(0)
