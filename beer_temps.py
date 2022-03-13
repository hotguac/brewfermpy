#!/usr/bin/python3

# Import 3rd party libraries ----------------------------------------
import tkinter as tk
import tkinter.font as font

# Import standard libraries -----------------------------------------

# Import application libraries --------------------------------------
import colors
import paths

from xchg import XchgData
from logger import BrewfermLogger


"""
Creates a rotating log
"""
logger = BrewfermLogger('beer_temps.py').getLogger()


# -------------------------------------------------------------------
#  Show current and target beer temps, adjust target beer temp
# -------------------------------------------------------------------
class gBeerTemps(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.xd = XchgData()  # read only for now

        self.create_widgets()
        self.update_temps()

    def create_widgets(self):
        self.current = tk.Label(self.master.values_box,
                                text="??",
                                background=colors.background,
                                fg=colors.normal50,
                                font=("Arial", -180)
                                )

        self.target = tk.Label(self.master.values_box,
                               text="??",
                               background=colors.background,
                               fg=colors.normal50,
                               font=("Arial", -80)
                               )

        self.button_font = font.Font(family="Arial", size=-60, weight="bold")

        self.warmer = tk.Button(
            self.master.values_box,
            text="+",
            command=self.plus_one,
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.warmer10 = tk.Button(
            self.master.values_box,
            text="10",
            command=self.plus_ten,
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.colder = tk.Button(
            self.master.values_box,
            text="-",
            command=self.minus_one,
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.colder10 = tk.Button(
            self.master.values_box,
            text="10",
            command=self.minus_ten,
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

    def update_temps(self):
        try:
            self.after(500, self.update_temps)

            beer_temp = self.xd.get(paths.beer_temp)
            if beer_temp is None:
                self.current['text'] = '??'
            else:
                self.current['text'] = str(round(beer_temp))

            beer_target = self.xd.get(paths.beer_target)
            if beer_target is None:
                self.target['text'] = '??'
            else:
                self.target['text'] = str(round(beer_target))

        except Exception as e:
            logger.exception("%s %s", type(e), e)

    def plus_one(self):
        self.master.beer_target += 1.0

    def plus_ten(self):
        self.master.beer_target += 10.0

    def minus_one(self):
        self.master.beer_target -= 1.0

    def minus_ten(self):
        self.master.beer_target -= 10.0

    def hide(self):
        self.warmer.place(x=0, y=0, height=0, width=0)
        self.warmer10.place(x=0, y=0, height=0, width=0)
        self.colder.place(x=0, y=0, height=0, width=0)
        self.colder10.place(x=0, y=0, height=0, width=0)
        self.current.place(x=0, y=0, height=0, width=0)
        self.target.place(x=0, y=0, height=0, width=0)

    def show_beer(self):
        self.warmer.place(x=0, y=0, height=0, width=0)
        self.warmer10.place(x=0, y=0, height=0, width=0)
        self.colder.place(x=0, y=0, height=0, width=0)
        self.colder10.place(x=0, y=0, height=0, width=0)

        self.current.place(x=160, y=80, height=200, width=320)
        self.target.place(x=580, y=120, height=100, width=160)

    def show_target(self):
        self.current.place(x=160, y=80, height=0, width=0)

        self.warmer.place(x=160, y=80, height=80, width=80)
        self.colder.place(x=160, y=180, height=80, width=80)
        self.warmer10.place(x=260, y=80, height=80, width=100)
        self.colder10.place(x=260, y=180, height=80, width=100)

        self.target.place(x=580, y=120, height=100, width=160)
