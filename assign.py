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
logger = BrewfermLogger('assign.py').getLogger()


# -------------------------------------------------------------------
#  Associate attached sensors to beer, chamber, or ambient temps
# -------------------------------------------------------------------
class gAssign(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.create_widgets()

        self.xd = XchgData()  # read only for now
        self.sensor_map = None
        self.sensors_raw = None

    def populate_widgets(self):
        slot = 0
        try:
            for id in self.sensors_raw:
                if id == 'ts':
                    continue

                if 'unknown' in id:
                    current_usage = 'spare'
                else:
                    current_usage = id

                if id != 'ts':
                    slot = slot + 1
                    if slot == 1:
                        self.func1['text'] = current_usage
                        for x in self.sensors_raw[id]:
                            self.id1['text'] = x
                            self.temp1['text'] = str(round(self.sensors_raw[id][x]))

                    if slot == 2:
                        self.func2['text'] = current_usage
                        for x in self.sensors_raw[id]:
                            self.id2['text'] = x
                            self.temp2['text'] = str(round(self.sensors_raw[id][x]))

                    if slot == 3:
                        self.func3['text'] = current_usage
                        for x in self.sensors_raw[id]:
                            self.id3['text'] = x
                            self.temp3['text'] = str(round(self.sensors_raw[id][x]))
        except Exception as e:
            logger.exception('%s', e)

    def create_widgets(self):
        normal_font = font.Font(family='DejaVu Sans Mono', size=-36)  # , weight='bold')

        self.id1 = tk.Label(self.master.values_box,
                            text='',
                            background=colors.background,
                            fg=colors.normal50,
                            anchor='w',
                            font=normal_font
                            )

        self.id2 = tk.Label(self.master.values_box,
                            text='',
                            background=colors.background,
                            fg=colors.normal50,
                            anchor='w',
                            font=normal_font
                            )

        self.id3 = tk.Label(self.master.values_box,
                            text='',
                            background=colors.background,
                            fg=colors.normal50,
                            anchor='w',
                            font=normal_font
                            )

        self.temp1 = tk.Label(self.master.values_box,
                              text="61",
                              background=colors.background,
                              fg=colors.normal50,
                              anchor='w',
                              font=normal_font
                              )

        self.temp2 = tk.Label(self.master.values_box,
                              text="62",
                              background=colors.background,
                              fg=colors.normal50,
                              anchor='w',
                              font=normal_font
                              )

        self.temp3 = tk.Label(self.master.values_box,
                              text='',
                              background=colors.background,
                              fg=colors.normal50,
                              anchor='w',
                              font=normal_font
                              )

        self.button_font = font.Font(family="Arial", size=-32, weight="bold")

        self.func1 = tk.Button(
            self.master.values_box,
            text='spare',
            command=self.store1,
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

        self.func2 = tk.Button(
            self.master.values_box,
            text='spare',
            command=self.store2,
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

        self.func3 = tk.Button(
            self.master.values_box,
            text='spare',
            command=self.store3,
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

    def get_new_function(self, slot, current_usage):
        beer_available = 1
        chamber_available = 1
        ambient_available = 1

        if slot == 1:
            if (self.func2['text'] == 'beer') or (self.func3['text'] == 'beer'):
                beer_available = 0
            if (self.func2['text'] == 'chamber') or (self.func3['text'] == 'chamber'):
                chamber_available = 0
            if (self.func2['text'] == 'ambient') or (self.func3['text'] == 'ambient'):
                ambient_available = 0

        if slot == 2:
            if (self.func1['text'] == 'beer') or (self.func3['text'] == 'beer'):
                beer_available = 0
            if (self.func1['text'] == 'chamber') or (self.func3['text'] == 'chamber'):
                chamber_available = 0
            if (self.func1['text'] == 'ambient') or (self.func3['text'] == 'ambient'):
                ambient_available = 0

        if slot == 3:
            if (self.func1['text'] == 'beer') or (self.func2['text'] == 'beer'):
                beer_available = 0
            if (self.func1['text'] == 'chamber') or (self.func2['text'] == 'chamber'):
                chamber_available = 0
            if (self.func1['text'] == 'ambient') or (self.func2['text'] == 'ambient'):
                ambient_available = 0

        if (current_usage == 'spare'):
            if (beer_available == 1):
                return 'beer'
            if (chamber_available == 1):
                return 'chamber'
            if (ambient_available == 1):
                return 'ambient'
            return 'spare'

        if (current_usage == 'beer'):
            if (chamber_available == 1):
                return 'chamber'
            if (ambient_available == 1):
                return 'ambient'
            return 'spare'

        if (current_usage == 'chamber'):
            if (ambient_available == 1):
                return 'ambient'
            return 'spare'

        if (current_usage == 'ambient'):
            return 'spare'

    def use_new_map(self):
        try:
            new_map = {}
            if (self.func1['text'] != 'spare') and (self.id1['text'] != ''):
                new_map[self.id1['text']] = self.func1['text']
            if (self.func2['text'] != 'spare') and (self.id2['text'] != ''):
                new_map[self.id2['text']] = self.func2['text']
            if (self.func3['text'] != 'spare') and (self.id3['text'] != ''):
                new_map[self.id3['text']] = self.func3['text']

            self.master.id_map = new_map
            self.master.update_out(reschedule=False)
        except Exception as e:
            logger.exception('%s', e)

    def store1(self):
        try:
            if self.id1['text'] != '':
                self.func1['text'] = self.get_new_function(1, self.func1['text'])
                self.use_new_map()
            else:
                self.func1['text'] = 'spare'
        except Exception as e:
            logger.exception('%s', e)

    def store2(self):
        try:
            if self.id2['text'] != '':
                self.func2['text'] = self.get_new_function(2, self.func2['text'])
                self.use_new_map()
            else:
                self.func2['text'] = 'spare'
        except Exception as e:
            logger.exception('%s', e)

    def store3(self):
        try:
            if self.id3['text'] != '':
                self.func3['text'] = self.get_new_function(3, self.func3['text'])
                self.use_new_map()
            else:
                self.func3['text'] = 'spare'
        except Exception as e:
            logger.exception('%s', e)

    def hide(self):
        self.id1.place(x=0, y=0, height=0, width=0)
        self.id2.place(x=0, y=0, height=0, width=0)
        self.id3.place(x=0, y=0, height=0, width=0)

        self.func1.place(x=0, y=0, height=0, width=0)
        self.func2.place(x=0, y=0, height=0, width=0)
        self.func3.place(x=0, y=0, height=0, width=0)

        self.temp1.place(x=0, y=0, height=0, width=0)
        self.temp2.place(x=0, y=0, height=0, width=0)
        self.temp3.place(x=0, y=0, height=0, width=0)

    def show(self):
        self.sensor_map = self.xd.get(paths.sensor_map)
        self.sensors_raw = self.xd.get(paths.sensors_raw)
        self.populate_widgets()

        self.id1.place(x=140, y=60, height=80, width=340)
        self.id2.place(x=140, y=120, height=80, width=340)
        self.id3.place(x=140, y=180, height=80, width=340)

        self.func1.place(x=500, y=80, height=40, width=220)
        self.func2.place(x=500, y=140, height=40, width=220)
        self.func3.place(x=500, y=200, height=40, width=220)

        self.temp1.place(x=740, y=60, height=80, width=80)
        self.temp2.place(x=740, y=120, height=80, width=80)
        self.temp3.place(x=740, y=180, height=80, width=80)
