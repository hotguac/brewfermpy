#!/usr/bin/python3

# Import 3rd party libraries --------------------------------------------------
import tkinter as tk

# Import standard libraries ---------------------------------------------------

# Import application libraries ------------------------------------------------
import colors
import paths

from xchg import XchgData
from logger import BrewfermLogger


"""
Creates a rotating log
"""
logger = BrewfermLogger('gui_bottom.py').getLogger()


class gBottom(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.chamber_temp = "XX"
        self.desired_state = "Xxxx"
        self.current_state = "Xxxx"

        self.xd = XchgData()  # we only need read in the bottom

        self.create_widgets()
        self.update_input()

    def update_input(self):
        try:
            self.master.after(6000, self.update_input)

            self.desired_state = self.xd.get(paths.desired)
            self.current_state = self.xd.get(paths.current)
            self.chamber_temp = self.xd.get(paths.chamber_temp, 0.0)

            self.chamber['text'] = round(self.chamber_temp)
            self.desired['text'] = self.desired_state
            self.current['text'] = self.current_state

        except Exception as e:
            logger.exception('%s %s', type(e), e)

    def create_widgets(self):
        #
        #       Heat/Cool Section (bottom)
        #
        self.heatcool = tk.Frame(self.master)
        self.heatcool["bg"] = colors.background
        self.heatcool.place(x=0, y=360, height=120, width=800)

        self.current = tk.Label(self.heatcool, text=paths.idle)
        self.current["bg"] = colors.background
        self.current["fg"] = colors.normal50
        self.current["font"] = ("Arial", -60)
        self.current.place(x=160, y=40, height=80, width=220)

        self.chamber = tk.Label(self.heatcool, text="99.9")
        self.chamber["bg"] = colors.background
        self.chamber["fg"] = colors.normal400
        self.chamber["font"] = ("Arial", -40)
        self.chamber.place(x=430, y=40, height=80, width=80)

        self.desired = tk.Label(self.heatcool, text="Cool")
        self.desired["bg"] = colors.background
        self.desired["fg"] = colors.cool200
        self.desired["font"] = ("Arial", -40)
        self.desired.place(x=580, y=40, height=80, width=160)

        # do the bar at top of heat/cool section
        self.title_bar = tk.Frame(self.heatcool)
        self.title_bar.place(x=160, y=0, height=40, width=640)
        self.title_bar['bg'] = colors.background

        self.image_tb = tk.PhotoImage(file=paths.resources + "top_bar.png")
        self.top_bar = tk.Label(self.title_bar, image=self.image_tb)
        self.top_bar.place(x=0, y=0, width=640, height=40)

        self.running = tk.Label(self.title_bar, text="Now")
        self.running["bg"] = colors.background
        self.running["fg"] = colors.invert_text
        self.running["font"] = ("Arial", -24)
        self.running.place(x=50, y=0, height=40, width=100)

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

        self.image_tc = tk.PhotoImage(file=paths.resources + "top_corner.png")
        self.top_corner = tk.Label(self.side_bar, image=self.image_tc)
        self.top_corner.place(x=0, y=0, width=160, height=60)

        self.image_lm = tk.PhotoImage(
            file=paths.resources + "bottom_bottom.png")
        self.left_middle = tk.Label(self.side_bar, image=self.image_lm)
        self.left_middle.place(x=0, y=60, width=160, height=60)
