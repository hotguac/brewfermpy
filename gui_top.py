#!/usr/bin/python3

# Import 3rd party libraries --------------------------------------------------
import tkinter as tk

# Import standard libraries ---------------------------------------------------
from datetime import datetime

# Import application libraries ------------------------------------------------
import colors
import paths
from logger import BrewfermLogger
from xchg import XchgData

"""
Creates a rotating log
"""
logger = BrewfermLogger('gui_top.py').getLogger()


class gTop(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.xd = XchgData()  # read only for now

        self.last_time = datetime.now().isoformat(sep=' ', timespec='seconds')
        self.create_widgets()

    def update_time(self):
        try:
            dt = datetime.now().isoformat(sep=' ', timespec='seconds')
            if (dt != self.last_time):
                self.date_time['text'] = dt
                self.last_time = dt
            self.date_time.after(500, self.update_time)
        except Exception as e:
            logger.exception("%s %s", type(e), e)

    def update_ambient(self):
        try:
            ambient_temp = self.xd.get(paths.ambient_temp)
            offset = self.xd.get(paths.ambient_temp_offset)
            if ambient_temp is None or offset is None:
                self.ambient_temp['text'] = ''
            else:
                at = ambient_temp + offset
                x = str(round(at)) + 'F'
                self.ambient_temp['text'] = x
            self.ambient_temp.after(5000, self.update_ambient)
        except Exception as e:
            logger.exception("%s %s", type(e), e)

    def create_widgets(self):
        #
        #   Screen Title Section (section)
        #
        self.title_box = tk.Frame(self.master)
        self.title_box["bg"] = colors.background

        self.image_left = tk.PhotoImage(file=paths.resources + "top_left.png")
        self.top_left = tk.Label(self.title_box, image=self.image_left)

        self.title = tk.Label(self.title_box, text="Brewferm v2.0.2")
        self.title["bg"] = colors.background
        self.title["font"] = ("Arial", -20)
        self.title["fg"] = colors.invert_text

        self.image_mid = tk.PhotoImage(file=paths.resources + "top_middle.png")
        self.top_mid = tk.Label(self.title_box, image=self.image_mid)
        self.top_mid2 = tk.Label(self.title_box, image=self.image_mid)

        self.date_time = tk.Label(self.title_box)
        self.date_time["bg"] = colors.background
        self.date_time["text"] = "2021-05-10 15:21:02"
        self.date_time["font"] = ("Arial", -20)
        self.date_time["fg"] = colors.invert_text

        self.image_right = tk.PhotoImage(
            file=paths.resources + "top_right.png")
        self.top_right = tk.Label(self.title_box, image=self.image_right)

        self.ambient_temp = tk.Label(self.title_box)
        self.ambient_temp["bg"] = colors.background
        self.ambient_temp["text"] = "??F"
        self.ambient_temp["font"] = ("Arial", -20)
        self.ambient_temp["fg"] = colors.invert_text

        self.title_box.place(x=0, y=0, height=40, width=800)

        self.top_left.place(x=0, y=0, height=40, width=80)
        self.title.place(x=80, y=0, height=36, width=180)
        self.top_mid.place(x=260, y=0, height=40, width=80)
        self.date_time.place(x=340, y=0, height=36, width=220)
        self.top_mid2.place(x=560, y=0, height=40, width=100)
        self.ambient_temp.place(x=660, y=0, height=36, width=60)
        self.top_right.place(x=720, y=0, height=40, width=80)

        self.update_time()
        self.update_ambient()
