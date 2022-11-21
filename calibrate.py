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
                if str(id) == 'ts':
                    continue

                self.full_ids.append(id)

                if id in self.sensor_map:
                    sensor_usage = self.sensor_map[id]
                else:
                    sensor_usage = 'spare'

                # TODO: set the offset
                offset = 0.0
                if sensor_usage == 'beer':
                    offset = self.xd.get(paths.beer_temp_offset)
                if sensor_usage == 'chamber':
                    offset = self.xd.get(paths.chamber_temp_offset)
                if sensor_usage == 'ambient':
                    offset = self.xd.get(paths.ambient_temp_offset)

                temperature = str(round(self.sensors_raw[id], 1))
                actual = str(round(self.sensors_raw[id] + offset, 1))

                slot = slot + 1
                if slot == 1:
                    self.role1['text'] = sensor_usage
                    self.sensor1['text'] = str(id)[-4:]
                    self.reported1['text'] = temperature
                    self.actual1['text'] = actual

                if slot == 2:
                    self.role2['text'] = sensor_usage
                    self.sensor2['text'] = str(id)[-4:]
                    self.reported2['text'] = temperature
                    self.actual2['text'] = actual

                if slot == 3:
                    self.role3['text'] = sensor_usage
                    self.sensor3['text'] = str(id)[-4:]
                    self.reported3['text'] = temperature
                    self.actual3['text'] = actual

        except Exception as e:
            logger.exception('%s', e)

    def create_widgets(self):
        normal_font = font.Font(family='DejaVu Sans Mono', size=-36)  # , weight='bold')

        self.sensor1 = tk.Label(self.master.values_box,
                                text='',
                                background=colors.background,
                                fg=colors.normal50,
                                anchor='w',
                                font=normal_font
                                )

        self.sensor2 = tk.Label(self.master.values_box,
                                text='',
                                background=colors.background,
                                fg=colors.normal50,
                                anchor='w',
                                font=normal_font
                                )

        self.sensor3 = tk.Label(self.master.values_box,
                                text='',
                                background=colors.background,
                                fg=colors.normal50,
                                anchor='w',
                                font=normal_font
                                )

        self.reported1 = tk.Label(self.master.values_box,
                                  text="61",
                                  background=colors.background,
                                  fg=colors.normal50,
                                  anchor='w',
                                  font=normal_font
                                  )

        self.reported2 = tk.Label(self.master.values_box,
                                  text="62",
                                  background=colors.background,
                                  fg=colors.normal50,
                                  anchor='w',
                                  font=normal_font
                                  )

        self.reported3 = tk.Label(self.master.values_box,
                                  text='',
                                  background=colors.background,
                                  fg=colors.normal50,
                                  anchor='w',
                                  font=normal_font
                                  )

        self.actual1 = tk.Label(self.master.values_box,
                                text="??.?",
                                background=colors.background,
                                fg=colors.normal50,
                                anchor='w',
                                font=normal_font
                                )

        self.actual2 = tk.Label(self.master.values_box,
                                text="??.?",
                                background=colors.background,
                                fg=colors.normal50,
                                anchor='w',
                                font=normal_font
                                )

        self.actual3 = tk.Label(self.master.values_box,
                                text='??.?',
                                background=colors.background,
                                fg=colors.normal50,
                                anchor='w',
                                font=normal_font
                                )

        self.button_font = font.Font(family="Arial", size=-32, weight="bold")

        self.role1 = tk.Label(
            self.master.values_box,
            text='spare',
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w'
            )

        self.role2 = tk.Label(
            self.master.values_box,
            text='spare',
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w'
            )

        self.role3 = tk.Label(
            self.master.values_box,
            text='spare',
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w'
            )

        self.s1_increase = tk.Button(
            self.master.values_box,
            text='+',
            command=lambda slot=1: self.increase(slot),
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w',
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.s1_decrease = tk.Button(
            self.master.values_box,
            text='-',
            command=lambda slot=1: self.decrease(slot),
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w',
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.s2_increase = tk.Button(
            self.master.values_box,
            text='+',
            command=lambda slot=2: self.increase(slot),
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w',
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.s2_decrease = tk.Button(
            self.master.values_box,
            text='-',
            command=lambda slot=2: self.decrease(slot),
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w',
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.s3_increase = tk.Button(
            self.master.values_box,
            text='+',
            command=lambda slot=3: self.increase(slot),
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w',
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.s3_decrease = tk.Button(
            self.master.values_box,
            text='-',
            command=lambda slot=3: self.decrease(slot),
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w',
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.reset_offsets = tk.Button(
            self.master.values_box,
            text='Zero Offsets',
            command=self.clear,
            foreground=colors.background,
            background=colors.cool50,
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
            background=colors.cool50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w',
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

    def increase(self, slot):
        try:
            id = self.full_ids[slot-1]
            if id in self.calibrations:
                offset = self.calibrations[id]
            else:
                offset = 0.0

            offset += 0.1

            self.calibrations[id] = offset
        except Exception as e:
            logger.exception('%s', e)

    def decrease(self, slot):
        try:
            id = self.full_ids[slot-1]
            if id in self.calibrations:
                offset = self.calibrations[id]
            else:
                offset = 0.0

            offset -= 0.1

            self.calibrations[id] = round(offset, 1)
        except Exception as e:
            logger.exception('%s', e)

    def clear(self):
        try:
            self.calibrations = {}
        except Exception as e:
            logger.exception('%s', e)

    def write(self):
        try:
            self.master.calibrations = self.calibrations
        except Exception as e:
            logger.exception('%s', e)

    def hide(self):
        self.sensor1.place(x=0, y=0, height=0, width=0)
        self.sensor2.place(x=0, y=0, height=0, width=0)
        self.sensor3.place(x=0, y=0, height=0, width=0)

        self.role1.place(x=0, y=0, height=0, width=0)
        self.role2.place(x=0, y=0, height=0, width=0)
        self.role3.place(x=0, y=0, height=0, width=0)

        self.reported1.place(x=0, y=0, height=0, width=0)
        self.reported2.place(x=0, y=0, height=0, width=0)
        self.reported3.place(x=0, y=0, height=0, width=0)

        self.actual1.place(x=0, y=0, height=0, width=0)
        self.actual2.place(x=0, y=0, height=0, width=0)
        self.actual3.place(x=0, y=0, height=0, width=0)

        self.s1_decrease.place(x=0, y=0, height=0, width=0)
        self.s1_increase.place(x=0, y=0, height=0, width=0)

        self.s2_decrease.place(x=0, y=0, height=0, width=0)
        self.s2_increase.place(x=0, y=0, height=0, width=0)

        self.s3_decrease.place(x=0, y=0, height=0, width=0)
        self.s3_increase.place(x=0, y=0, height=0, width=0)

        self.reset_offsets.place(x=0, y=0, height=0, width=0)
        self.write_offsets.place(x=0, y=0, height=0, width=0)

    def show(self):
        self.populate_widgets()

        self.sensor1.place(x=140, y=30, height=80, width=100)
        self.sensor2.place(x=140, y=90, height=80, width=100)
        self.sensor3.place(x=140, y=150, height=80, width=100)

        self.role1.place(x=250, y=50, height=40, width=170)
        self.role2.place(x=250, y=110, height=40, width=170)
        self.role3.place(x=250, y=170, height=40, width=170)

        self.reported1.place(x=440, y=30, height=80, width=100)
        self.reported2.place(x=440, y=90, height=80, width=100)
        self.reported3.place(x=440, y=150, height=80, width=100)

        self.actual1.place(x=560, y=30, height=80, width=100)
        self.actual2.place(x=560, y=90, height=80, width=100)
        self.actual3.place(x=560, y=150, height=80, width=100)

        self.s1_increase.place(x=670, y=40, height=50, width=40)
        self.s2_increase.place(x=670, y=100, height=50, width=40)
        self.s3_increase.place(x=670, y=160, height=50, width=40)

        self.s1_decrease.place(x=740, y=40, height=50, width=40)
        self.s2_decrease.place(x=740, y=100, height=50, width=40)
        self.s3_decrease.place(x=740, y=160, height=50, width=40)

        self.reset_offsets.place(x=200, y=230, height=50, width=220)
        self.write_offsets.place(x=480, y=230, height=50, width=240)
