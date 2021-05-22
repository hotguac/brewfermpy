#!/usr/bin/python3

# Import 3rd party libraries --------------------------------------------------
import tkinter as tk
import tkinter.font as font

# Import standard libraries ---------------------------------------------------
import atexit
import logging
import math
#import mmap
import os
import random
import signal
import sys

from datetime import datetime

# Import application libraries ------------------------------------------------
import colors
import paths

from xchg import Xchg


class gMiddle(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        self.beer_temp = "64.8"
        self.beer_target = "65.0"
        self.sensors_out = Xchg(paths.sensors_out, 'r', default={})

        self.create_widgets()

    def get_current(self):
        try:
            return self.beer_temp[0:2]
        except Exception as e:
            logging.exception("%s %s",type(e), e)

    def get_cdecimal(self):
        try:
            return self.beer_temp[2:4]
        except Exception as e:
            logging.exception("%s %s",type(e), e)

    def get_target(self):
        try:
            return self.beer_target[:2]
        except Exception as e:
            logging.exception("%s %s",type(e), e)

    def update_temps(self):
        try:
            self.after(30000, self.update_temps)
            
            #self.get_sensor_readings()
            x = self.sensors_out.read()

            self.current['text'] = self.get_current()
            self.cdecimal['text'] = self.get_cdecimal()
            self.target['text'] = self.get_target()
        except Exception as e:
            logging.exception("%s %s",type(e), e)

    def pause_brew(self):
        try:
            if self.pause_button['text'] == "Pause":
                logging.warning("brewing paused...")
                self.pause_button['text'] = "Resume"
            else:
                logging.warning("brewing resumeed...")
                self.pause_button['text'] = "Pause"

        except Exception as e:
            logging.exception(e)

    def exit_brew(self):
        logging.info("exiting gui")
        self.master.destroy()

    def rotate(self):
        try:
            logging.info("rotate")

            x = self.rotate_button['bg']

            if x == colors.normal_button:
                self.rotate_button['bg'] = colors.warm800
            else :
                self.rotate_button['bg'] = colors.normal_button
        except Exception as e:
            logging.exception("rotate %s %s", type(e), e)

    def create_widgets(self):
        self.values_box = tk.Frame(self.master)
        self.values_box['bg'] = colors.background
        self.values_box.place(x=0,y=40,height=320,width=800)
        self.values_box.after(2000,self.update_temps)

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

        self.pause_button = tk.Button(self.button_box, text="Pause")
        self.pause_button['command'] = self.pause_brew
        self.pause_button['bg'] = colors.normal_button
        self.pause_button["font"] = self.button_font
        self.pause_button['activebackground'] = colors.normal_button
        self.pause_button['highlightbackground'] = colors.normal_button
        self.pause_button['highlightcolor'] = colors.normal_button
        self.pause_button['relief'] = tk.FLAT
        self.pause_button.place(x=10, y=70, height=52, width=110)

        self.settings_button = tk.Button(self.button_box, text="Settings", command=self.rotate)
        self.settings_button['bg'] = colors.normal_button
        self.settings_button["font"] = self.button_font
        self.settings_button['activebackground'] = colors.normal_button
        self.settings_button['highlightbackground'] = colors.normal_button
        self.settings_button['highlightcolor'] = colors.normal_button
        self.settings_button['relief'] = tk.FLAT
        self.settings_button.place(x=10, y=134, height=52, width=110)

        self.exit_button = tk.Button(self.button_box, text="Exit", command=self.exit_brew)
        self.exit_button['bg'] = colors.normal_button
        self.exit_button["font"] = self.button_font
        self.exit_button['activebackground'] = colors.normal_button
        self.exit_button['highlightbackground'] = colors.normal_button
        self.exit_button['highlightcolor'] = colors.normal_button
        self.exit_button['relief'] = tk.FLAT
        self.exit_button.place(x=10, y=198, height=52, width=110)

        self.image_bb = tk.PhotoImage(file = paths.resources + "bottom_bar.png")
        self.bottom_bar = tk.Label(self.values_box, image=self.image_bb)
        self.bottom_bar.place(x=160, y=280, width=640, height=40)

        self.image_tb = tk.PhotoImage(file = paths.resources + "top_bar.png")
        self.top_bar = tk.Label(self.values_box, image=self.image_tb)
        self.top_bar.place(x=160, y=0, width=640, height=40)

        self.lbl_current = tk.Label(self.values_box, text="Temp F")
        self.lbl_current["bg"] = colors.background
        self.lbl_current["fg"] = colors.invert_text
        self.lbl_current["font"] = ("Arial", -24)
        self.lbl_current.place(x=220, y=0, height=40, width=160)

        self.lbl_target = tk.Label(self.values_box, text="Target F")
        self.lbl_target["bg"] = colors.background
        self.lbl_target["fg"] = colors.invert_text
        self.lbl_target["font"] = ("Arial", -24)
        self.lbl_target.place(x=580, y=0, height=40, width=160)

        self.current = tk.Label(self.values_box, text="64")
        self.current["bg"] = colors.background
        self.current["fg"] = colors.normal50
        self.current["font"] = ("Arial", -180)
        self.current.place(x=160, y=60, height=190, width=260)
        
        self.cdecimal = tk.Label(self.values_box, text=".3")
        self.cdecimal["bg"] = colors.background
        self.cdecimal["fg"] = colors.normal50
        self.cdecimal["font"] = ("Arial", -70)
        self.cdecimal.place(x=400, y=160, height=70, width=70)
        
        self.target = tk.Label(self.values_box, text="64")
        self.target["bg"] = colors.background
        self.target["fg"] = colors.normal50
        self.target["font"] = ("Arial", -90)
        self.target.place(x=580, y=110, height=100, width=160)
        
