#!/usr/bin/python3

# Import 3rd party libraries --------------------------------------------------
import tkinter as tk
from PIL import ImageTk, Image

# Import standard libraries ---------------------------------------------------
import atexit
import logging
import math
import os
import signal
import sys

from datetime import datetime

# Import application libraries ------------------------------------------------
import colors
import paths

class gTop(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.last_time = datetime.now().isoformat(sep=' ', timespec='seconds')
        self.pack()
        self.create_widgets()
        
    def update_time(self):
        try:
            dt = datetime.now().isoformat(sep=' ', timespec='seconds')
            if (dt != self.last_time):                     
                self.date_time['text'] = dt
                self.last_time = dt
            self.date_time.after(500, self.update_time)            
        except Exception as e:
            logging.exception("%s %s",type(e), e)

    def create_widgets(self):
        #
        #   Screen Title Section (section)
        #
        self.title_box = tk.Frame(self.master)
        self.title_box["bg"] = colors.background
        self.title_box.place(x=0,y=0,height=40,width=800)

        self.image_left = tk.PhotoImage(file = paths.resources + "top_left.png")
        self.top_left = tk.Label(self.title_box, image=self.image_left)
        self.top_left.place(x=0, y=0, width=80, height=40)

        self.title = tk.Label(self.title_box, text="Brewferm v2.0.1")
        self.title["bg"] = colors.background
        self.title["font"] = ("Arial", -20)
        self.title["fg"] = colors.invert_text
        self.title.place(x=80,y=0,height=36,width=200)
        
        self.image_mid = tk.PhotoImage(file = paths.resources + "top_middle.png")
        self.top_mid = tk.Label(self.title_box, image=self.image_mid)
        self.top_mid.place(x=280, y=0, width=160, height=40)
        self.top_mid2 = tk.Label(self.title_box, image=self.image_mid)
        self.top_mid2.place(x=330, y=0, width=160, height=40)

        self.date_time = tk.Label(self.title_box)
        self.date_time["bg"] = colors.background
        self.date_time["text"] = "2021-05-10 15:21:02"
        self.date_time["font"] = ("Arial", -20)
        self.date_time["fg"] = colors.invert_text
        self.update_time()
        self.date_time.after(1000, self.update_time)
        self.date_time.place(x=460,y=0, height=36, width=280)

        self.image_right = tk.PhotoImage(file = paths.resources + "top_right.png")
        self.top_right = tk.Label(self.title_box, image=self.image_right)
        self.top_right.place(x=720, y=0, width=80, height=40)

        