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
logger = BrewfermLogger('calibrate.py').getLogger()


# -------------------------------------------------------------------
#  Associate attached sensors to beer, chamber, or ambient temps
# -------------------------------------------------------------------
class gCalibrate(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.create_widgets()

        self.xd = XchgData()  # read only for now
        self.calibrations = self.xd.get(paths.calibrations, {})
        self.sensor_map = self.xd.get(paths.sensor_map)

        self.full_ids = []

    def populate_widgets(self):
        self.sensors_raw = self.xd.get(paths.sensors_raw)

        slot = 0
        try:
            for id in self.sensors_raw:
                if str(id) == 'ts' or slot == 3:
                    continue

                self.full_ids.append(id)

                if id in self.sensor_map:
                    sensor_usage = self.sensor_map[id]
                else:
                    sensor_usage = 'spare'

                if id in self.calibrations:
                    offset = self.calibrations[id]
                else:
                    offset = 0.0

                temperature = str(round(self.sensors_raw[id], 1))
                actual = str(round(self.sensors_raw[id] + offset, 1))

                self.sensor_id_short[slot]['text'] = str(id)[-4:]
                self.reported[slot]['text'] = temperature
                self.actual[slot]['text'] = actual
                self.role[slot]['text'] = sensor_usage

                slot = slot + 1
        except Exception as e:
            logger.exception('%s', e)

    def create_widgets(self):
        try:
            normal_font = font.Font(family='DejaVu Sans Mono', size=-36)  # , weight='bold')
            self.button_font = font.Font(family="Arial", size=-32, weight="bold")

            self.sensor_id_short = []
            self.reported = []
            self.actual = []
            self.role = []
            self.increase_btn = []
            self.decrease_btn = []

            for slot in range(3):
                self.sensor_id_short.append(
                    tk.Label(
                        self.master.values_box,
                        text='',
                        background=colors.background,
                        fg=colors.normal50,
                        anchor='w',
                        font=normal_font
                        ))

                self.reported.append(
                    tk.Label(
                        self.master.values_box,
                        text="61",
                        background=colors.background,
                        fg=colors.normal50,
                        anchor='w',
                        font=normal_font
                        ))

                self.actual.append(
                    tk.Label(
                        self.master.values_box,
                        text='??.?',
                        background=colors.background,
                        fg=colors.cool200,
                        anchor='w',
                        font=normal_font
                        ))

                self.role.append(
                    tk.Label(
                        self.master.values_box,
                        text='spare',
                        foreground=colors.background,
                        background=colors.normal50,
                        borderwidth=0,
                        highlightthickness=0,
                        font=self.button_font,
                        anchor='w'
                        ))

                self.increase_btn.append(
                    tk.Button(
                        self.master.values_box,
                        text='+',
                        foreground=colors.background,
                        background=colors.cool200,
                        borderwidth=0,
                        highlightthickness=0,
                        font=self.button_font,
                        anchor='w',
                        activebackground=colors.normal_button,
                        highlightbackground=colors.normal_button,
                        highlightcolor=colors.normal_button,
                        relief=tk.FLAT
                        ))

                self.increase_btn[slot].config(command=lambda slot=slot: self.increase(slot))

                self.decrease_btn.append(
                        tk.Button(
                            self.master.values_box,
                            text='-',
                            foreground=colors.background,
                            background=colors.cool200,
                            borderwidth=0,
                            highlightthickness=0,
                            font=self.button_font,
                            anchor='w',
                            activebackground=colors.normal_button,
                            highlightbackground=colors.normal_button,
                            highlightcolor=colors.normal_button,
                            relief=tk.FLAT
                            ))

                self.decrease_btn[slot].config(command=lambda slot=slot: self.decrease(slot))

            self.reset_offsets = tk.Button(
                self.master.values_box,
                text='Zero Offsets',
                command=self.clear,
                foreground=colors.background,
                background=colors.warm50,
                borderwidth=0,
                highlightthickness=0,
                font=self.button_font,
                anchor='w',
                activebackground=colors.normal_button,
                highlightbackground=colors.normal_button,
                highlightcolor=colors.normal_button,
                relief=tk.FLAT
                )

            self.write_offsets = tk.Button(
                self.master.values_box,
                text='Save Offsets',
                command=self.write,
                foreground=colors.background,
                background=colors.warm50,
                borderwidth=0,
                highlightthickness=0,
                font=self.button_font,
                anchor='w',
                activebackground=colors.normal_button,
                highlightbackground=colors.normal_button,
                highlightcolor=colors.normal_button,
                relief=tk.FLAT
                )
        except Exception as e:
            logger.exception('%s', e)

    def increase(self, slot):
        try:
            id = self.full_ids[slot]
            if id in self.calibrations:
                offset = self.calibrations[id]
            else:
                offset = 0.0

            offset = round(offset + 0.1, 1)

            self.calibrations[id] = offset
            self.populate_widgets()
        except Exception as e:
            logger.exception('%s', e)

    def decrease(self, slot):
        try:
            id = self.full_ids[slot]
            if id in self.calibrations:
                offset = self.calibrations[id]
            else:
                offset = 0.0

            offset = round(offset - 0.1, 1)

            self.calibrations[id] = round(offset, 1)
            self.populate_widgets()
        except Exception as e:
            logger.exception('%s', e)

    def clear(self):
        try:
            self.calibrations = {}
            self.populate_widgets()
        except Exception as e:
            logger.exception('%s', e)

    def write(self):
        try:
            self.master.calibrations = self.calibrations
        except Exception as e:
            logger.exception('%s', e)

    def hide(self):
        try:
            for slot in range(3):
                self.sensor_id_short[slot].place(x=0, y=0, height=0, width=0)
                self.role[slot].place(x=0, y=0, height=0, width=0)
                self.reported[slot].place(x=0, y=0, height=0, width=0)
                self.actual[slot].place(x=0, y=0, height=0, width=0)
                self.increase_btn[slot].place(x=0, y=0, height=0, width=0)
                self.decrease_btn[slot].place(x=0, y=0, height=0, width=0)

            self.reset_offsets.place(x=0, y=0, height=0, width=0)
            self.write_offsets.place(x=0, y=0, height=0, width=0)
        except Exception as e:
            logger.exception('%s', e)

    def show(self):
        try:
            self.populate_widgets()

            for slot in range(3):
                self.sensor_id_short[slot].place(x=140, y=30+(slot*60), height=80, width=100)
                self.role[slot].place(x=250, y=50+(slot*60), height=40, width=170)
                self.reported[slot].place(x=440, y=30+(slot*60), height=80, width=100)
                self.actual[slot].place(x=560, y=30+(slot*60), height=80, width=100)
                self.increase_btn[slot].place(x=670, y=40+(slot*60), height=50, width=40)
                self.decrease_btn[slot].place(x=740, y=40+(slot*60), height=50, width=40)

            self.reset_offsets.place(x=200, y=230, height=50, width=220)
            self.write_offsets.place(x=480, y=230, height=50, width=240)
        except Exception as e:
            logger.exception('%s', e)
