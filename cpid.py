#!/usr/bin/python3

# Import 3rd party libraries ----------------------------------------
import tkinter as tk
import tkinter.font as font

# Import standard libraries -----------------------------------------
import logging

# Import application libraries --------------------------------------
# import colors
# import paths

from xchg import XchgData


# -------------------------------------------------------------------
#  Associate attached sensors to beer, chamber, or ambient temps
# -------------------------------------------------------------------
class gCPID(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.create_widgets()

        self.xd = XchgData()  # read only for now

        self.visible = False
        self.populate_widgets()

    def populate_widgets(self):
        logging.debug("populate_widgets")

    def create_widgets(self):
        normal_font = font.Font(family='DejaVu Sans Mono', size=-36)  # , weight='bold')

    def hide(self):
        logging.debug("gPBID hide")
        self.visible = False

    def show(self):
        self.visible = True
        self.populate_widgets()
        logging.debug("gBIPD show")
