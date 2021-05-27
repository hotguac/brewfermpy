#!/usr/bin/python3

# Import 3rd party libraries --------------------------------------------------
import tkinter as tk

# Import standard libraries ---------------------------------------------------
import logging
import os
import sys

#from datetime import datetime

# Import application libraries ------------------------------------------------
import colors
import paths

from gui_top import gTop
from gui_middle import gMiddle
from gui_bottom import gBottom

# Functions -------------------------------------------------------------------
# make sure there is an environment variable for DISPLAY
# so we can run the GUI
def check_display():
    if os.environ.get('DISPLAY','') == '':
        logging.warning('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')
    else:
        logging.info(os.environ.get('DISPLAY',''))

# App -------------------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG, filename=paths.logs, format='%(asctime)s-%(process)d-gui.py     -%(levelname)s - %(message)s')
logging.info("gui starting up")

try:
    check_display()

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg=colors.background)
    root.configure(cursor="none")

    root.update_idletasks()
    logging.info("Canvas Size = height %d and width %d",root.winfo_height(), root.winfo_width())

except _tkinter.TclError as e:
    logging.info("display not ready yet...")
    sys.exit(1)

except Exception as e:
    logging.exception("%s %s",type(e), e)
    sys.exit(1)

#
#   Widgets ---------------------------------------------------------------------
#
try:
    tg = gTop(master=root)
    gm = gMiddle(master=root)
    bg = gBottom(master=root)   
except Exception as e:
    logging.exception("%s %s",type(e), e)

#
#   Display ---------------------------------------------------------------------
#
try:
    root.mainloop()
except Exception as e:
    logging.exception("%s %s",type(e), e)
