#!/usr/bin/python3

# Import 3rd party libraries ----------------------------------------
import tkinter as tk
import tkinter.font as font

# Import standard libraries -----------------------------------------

# Import application libraries --------------------------------------
import colors
from logger import BrewfermLogger


"""
Creates a rotating log
"""
logger = BrewfermLogger('settings.py').getLogger()


# -------------------------------------------------------------------
# Allow user to change system settings
# -------------------------------------------------------------------
class gMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.create_widgets()
        self.update_ok()

    def create_widgets(self):
        self.button_font = font.Font(family="Arial", size=-20, weight="bold")

        self.target = tk.Button(
            self.master.values_box,
            text="Target Temp",
            command=self.set_beer_target,
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

        self.sensor_assign = tk.Button(
            self.master.values_box,
            text="Assign Sensors",
            command=self.assign_sensors,
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

        self.bPIDsettings = tk.Button(
            self.master.values_box,
            text="Beer PID",
            command=self.set_beer_pid,
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

        self.cPIDsettings = tk.Button(
            self.master.values_box,
            text="Chamber PID",
            command=self.set_chamber_pid,
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

    def update_ok(self):
        try:
            self.after(500, self.update_ok)

        except Exception as e:
            logger.exception("%s %s", type(e), e)

    def set_beer_target(self):
        self.hide()
        self.master.btemps.show_target()

    def assign_sensors(self):
        self.hide()
        self.master.sensor_assign.show()

    def set_beer_pid(self):
        self.hide()
        self.master.bpid_settings.show()

    def set_chamber_pid(self):
        self.hide()
        self.master.cpid_settings.show()

    def hide(self):
        self.target.place(x=0, y=0, height=0, width=0)
        self.sensor_assign.place(x=0, y=0, height=0, width=0)
        self.bPIDsettings.place(x=0, y=0, height=0, width=0)
        self.cPIDsettings.place(x=0, y=0, height=0, width=0)

    def show(self):
        self.target.place(x=180, y=60, height=80, width=200)
        self.sensor_assign.place(x=440, y=60, height=80, width=200)
        self.bPIDsettings.place(x=180, y=160, height=80, width=200)
        self.cPIDsettings.place(x=440, y=160, height=80, width=200)
