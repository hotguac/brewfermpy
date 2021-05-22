#!/usr/bin/python3

# Import 3rd party libraries --------------------------------------------------
import tkinter as tk
from PIL import Image, ImageTk

# Import standard libraries ---------------------------------------------------
import atexit
import logging
import math
import mmap
import os
import signal
import sys

from datetime import datetime

# Import application libraries ------------------------------------------------
import colors
import paths

from xchg import Xchg

class gBottom(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.beer_chamber = "65.9"
        self.sensors_out = Xchg(paths.sensors_out, 'r', default={})
        self.relays_out = Xchg(paths.relays_out, 'r', default={})
        
        self.create_widgets()
        self.update_chamber()

    def update_chamber(self):
        try:
            self.master.after(6000, self.update_chamber)
            self.chamber['text'] = self.beer_chamber
        except Exception as e:
            logging.exception("update_chamber")

    def create_widgets(self):
        #
        #       Heat/Cool Section (bottom)
        #
        self.heatcool = tk.Frame(self.master)
        self.heatcool["bg"] = colors.background
        self.heatcool.place(x=0, y=360, height=120, width=800)

        self.current = tk.Label(self.heatcool, text="Idle")
        self.current["bg"] = colors.background
        self.current["fg"] = colors.normal50
        self.current["font"] = ("Arial", -60)
        self.current.place(x=200, y=40, height=80, width=160)
        
        self.chamber = tk.Label(self.heatcool, text="99.9")
        self.chamber["bg"] = colors.background
        self.chamber["fg"] = colors.normal400
        self.chamber["font"] = ("Arial", -30)
        self.chamber.place(x=430, y=40, height=80, width=80)
        
        self.hc_target = tk.Label(self.heatcool, text="Cool")
        self.hc_target["bg"] = colors.background
        self.hc_target["fg"] = colors.cool200
        self.hc_target["font"] = ("Arial", -40)
        self.hc_target.place(x=580, y=40, height=80, width=160)

        # do the bar at top of heat/cool section
        self.title_bar = tk.Frame(self.heatcool)
        self.title_bar.place(x=160, y=0, height=40, width=640)
        self.title_bar['bg'] = colors.background

        self.image_tb = tk.PhotoImage(file = paths.resources + "top_bar.png")
        self.top_bar = tk.Label(self.title_bar, image=self.image_tb)
        self.top_bar.place(x=0, y=0, width=640, height=40)

        self.running = tk.Label(self.title_bar, text="Now")
        self.running["bg"] = colors.background
        self.running["fg"] = colors.invert_text
        self.running["font"] = ("Arial", -24)
        self.running.place(x=70, y=0, height=40, width=100)
        
        self.lbl_chamber = tk.Label(self.title_bar, text="Chamber F")
        self.lbl_chamber["bg"] = colors.background
        self.lbl_chamber["fg"] = colors.invert_text
        self.lbl_chamber["font"] = ("Arial", -16)
        self.lbl_chamber.place(x=260, y=0, height=40, width=110)
        
        self.target = tk.Label(self.title_bar, text="Desired")
        self.target["bg"] = self.title_bar["bg"]
        self.target["fg"] = colors.invert_text
        self.target["font"] = ("Arial", -24)
        self.target.place(x=440, y=0, height=40, width=120)

        # Side Bar
        self.side_bar = tk.Frame(self.heatcool)
        self.side_bar['bg'] = colors.background
        self.side_bar.place(x=0, y=0, height=120, width=160)

        self.image_tc = tk.PhotoImage(file = paths.resources + "top_corner.png")
        self.top_corner = tk.Label(self.side_bar, image=self.image_tc)
        self.top_corner.place(x=0, y=0, width=160, height=60)

        self.image_lm = tk.PhotoImage(file = paths.resources + "bottom_bottom.png")
        self.left_middle = tk.Label(self.side_bar, image=self.image_lm)
        self.left_middle.place(x=0, y=60, width=160, height=60)

    