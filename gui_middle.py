#!/usr/bin/python3

# Import 3rd party libraries --------------------------------------------------
import tkinter as tk
import tkinter.font as font

# Import standard libraries ---------------------------------------------------
import atexit
import logging
import math
import os
import random
import signal
import sys

from datetime import datetime

# Import application libraries ------------------------------------------------
import colors
import paths

from xchg import Xchg, XchgData

#--------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------
class gBeerTemps(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.beer_temp = "64.8"
        self.beer_target = "65.0"
        
        self.xd = XchgData() # read only for now

        self.create_widgets()
        self.update_temps()

    def update_temps(self):
        try:
            self.after(1000, self.update_temps)
            self.beer_temp = self.xd.get_beer_temp()
            self.beer_target = self.xd.get_target_temp() 
            
            self.current['text'] = str(round(self.beer_temp))
            self.target['text'] = str(round(self.beer_target))
        except Exception as e:
            logging.exception("%s %s",type(e), e)

    def create_widgets(self):
        self.current = tk.Label(self.master.values_box, text="64")
        self.current["bg"] = colors.background
        self.current["fg"] = colors.normal50
        self.current["font"] = ("Arial", -180)
        self.current.place(x=160, y=80, height=200, width=240)

        self.target = tk.Label(self.master.values_box, text="64")
        self.target["bg"] = colors.background
        self.target["fg"] = colors.normal50
        self.target["font"] = ("Arial", -80)
        self.target.place(x=580, y=120, height=100, width=160)

# ---------------------------------------------------------------------------------------------------------        
# 
# ---------------------------------------------------------------------------------------------------------        
class gMiddle(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.set_initial_state()      
        self.xd = XchgData(paths.gui_out)
       
        self.master = master
        self.create_widgets()
        
        self.btemps = None

        self.after(10000, self.update_out)
        
    def set_initial_state(self):
        self.beer_temp = "64.8"
        self.beer_target = "65.0"
        self.state = paths.running

    def update_out(self):
        try:
            self.after(1000, self.update_out)

            if self.btemps is None:
                self.btemps = gBeerTemps(master=self)

            self.xd.write_gui(self.format_state())
        except Exception as e:
            logging.exception('%s %s', type(e), e)
                  
    def format_state(self):
        x = {}
        x[paths.beer_target] = self.beer_target
        x[paths.state] = self.state

        return x

    def pause_brew(self):
        try:
            if self.pause_button['text'] == "Pause":
                logging.warning("brewing paused...")
                self.state = paths.paused
                self.pause_button['text'] = "Resume"
            else:
                logging.info("brewing resumeed...")
                self.pause_button['text'] = "Pause"
                self.state = paths.running

        except Exception as e:
            logging.exception(e)

    def exit_brew(self):
        logging.info("exiting gui")
        self.master.destroy()

    def settings(self):
        try:
            logging.info('settings')
        except Exception as e:
            logging.exception("settings %s %s", type(e), e)

    def create_widgets(self):
        self.values_box = tk.Frame(self.master)
        self.values_box['bg'] = colors.background
        self.values_box.place(x=0,y=40,height=320,width=800)

        self.title_box = tk.Frame(self.values_box)
        self.title_box.place(x=160,y=0,height=40,width=640)
        self.title_box['bg'] = colors.background

        self.button_box = tk.Frame(self.values_box)
        self.button_box['bg'] = colors.background
        self.button_box.place(x=0,y=0,height=320,width=160)

        self.image_tc = tk.PhotoImage(file = paths.resources + "top_corner.png")
        self.top_corner = tk.Label(self.button_box, image=self.image_tc)
        self.top_corner.place(x=0, y=0, width=160, height=60)

        self.image_bc = tk.PhotoImage(file = paths.resources + "bottom_corner.png")
        self.bottom_corner = tk.Label(self.button_box, image=self.image_bc)
        self.bottom_corner.place(x=0, y=260, width=160, height=60)

        self.button_font = font.Font(family="Arial", size=-18, weight="normal")

        self.pause_button = tk.Button(
            self.button_box, 
            text="Pause",
            command = self.pause_brew,
            bg = colors.normal_button,
            font = self.button_font,
            activebackground = colors.normal_button,
            highlightbackground = colors.normal_button,
            highlightcolor = colors.normal_button,
            relief = tk.FLAT
            )

        self.pause_button.place(x=10, y=70, height=52, width=110)

        self.settings_button = tk.Button(
            self.button_box, 
            text="Settings", 
            command=self.settings,
            background = colors.normal_button,
            borderwidth = 0,
            highlightthickness = 0,
            font = self.button_font,
            activebackground = colors.normal_button,
            highlightbackground = colors.normal_button,
            highlightcolor = colors.normal_button,
            relief = tk.FLAT
            )

        self.settings_button.place(x=10, y=134, height=52, width=110)

        self.exit_button = tk.Button(
            self.button_box, 
            text="Exit", 
            command=self.exit_brew,
            background = colors.normal_button,
            borderwidth = 0,
            highlightthickness = 0,
            font = self.button_font,
            activebackground = colors.normal_button,
            highlightbackground = colors.normal_button,
            highlightcolor = colors.normal_button,
            relief = tk.FLAT
            )

        self.exit_button.place(x=10, y=198, height=52, width=110)

        self.image_bb = tk.PhotoImage(file = paths.resources + "bottom_bar.png")
        self.bottom_bar = tk.Label(self.values_box, image=self.image_bb)
        self.bottom_bar.place(x=160, y=280, width=640, height=40)

        self.image_tb = tk.PhotoImage(file = paths.resources + "top_bar.png")
        self.top_bar = tk.Label(self.values_box, image=self.image_tb)
        self.top_bar.place(x=160, y=0, width=640, height=40)

        self.lbl_current = tk.Label(
            self.values_box, 
            text="Temp F",
            bg = colors.background,
            fg = colors.invert_text,
            font = ("Arial", -24)
            )

        self.lbl_current.place(x=220, y=0, height=40, width=160)

        self.lbl_target = tk.Label(self.values_box, text="Target F")
        self.lbl_target["bg"] = colors.background
        self.lbl_target["fg"] = colors.invert_text
        self.lbl_target["font"] = ("Arial", -24)
        self.lbl_target.place(x=580, y=0, height=40, width=160)
