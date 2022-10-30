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
        self.sensor_map = None
        self.sensors_raw = None

        self.sensor1 = None
        self.sensor2 = None
        self.sensor3 = None

        self.s1_offset = 0

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
                            self.sensor1 = x
                            self.id1['text'] = str(x)[-4:]
                            self.temp1['text'] = str(round(self.sensors_raw[id][x], 1))

                    if slot == 2:
                        self.func2['text'] = current_usage
                        for x in self.sensors_raw[id]:
                            self.sensor2 = x
                            self.id2['text'] = str(x)[-4:]
                            self.temp2['text'] = str(round(self.sensors_raw[id][x], 1))

                    if slot == 3:
                        self.func3['text'] = current_usage
                        for x in self.sensors_raw[id]:
                            self.sensor3 = x
                            self.id3['text'] = str(x)[-4:]
                            self.temp3['text'] = str(round(self.sensors_raw[id][x], 1))
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

        self.temp1a = tk.Label(self.master.values_box,
                               text="61.0",
                               background=colors.background,
                               fg=colors.normal50,
                               anchor='w',
                               font=normal_font
                               )

        self.temp2a = tk.Label(self.master.values_box,
                               text="62.8",
                               background=colors.background,
                               fg=colors.normal50,
                               anchor='w',
                               font=normal_font
                               )

        self.temp3a = tk.Label(self.master.values_box,
                               text='63.4',
                               background=colors.background,
                               fg=colors.normal50,
                               anchor='w',
                               font=normal_font
                               )

        self.button_font = font.Font(family="Arial", size=-32, weight="bold")

        self.func1 = tk.Label(
            self.master.values_box,
            text='spare',
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w'
            )

        self.func2 = tk.Label(
            self.master.values_box,
            text='spare',
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w'
            )

        self.func3 = tk.Label(
            self.master.values_box,
            text='spare',
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            anchor='w'
            )

        self.s1_plus = tk.Button(
            self.master.values_box,
            text='+',
            command=self.increase_s1,
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

        self.s1_minus = tk.Button(
            self.master.values_box,
            text='-',
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

        self.s2_plus = tk.Button(
            self.master.values_box,
            text='+',
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

        self.s2_minus = tk.Button(
            self.master.values_box,
            text='-',
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

        self.s3_plus = tk.Button(
            self.master.values_box,
            text='+',
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

        self.s3_minus = tk.Button(
            self.master.values_box,
            text='-',
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

        self.clear_saved = tk.Button(
            self.master.values_box,
            text='Clear All',
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
            text='Write Offsets',
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

        # self.back_button = tk.Button(
        #     self.master.button_box,
        #     text="Back",
        #     command=self.settings,
        #     background=colors.normal_button,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     font=normal_font, # self.button_font,
        #     activebackground=colors.normal_button,
        #     highlightbackground=colors.normal_button,
        #     highlightcolor=colors.normal_button,
        #     relief=tk.FLAT
        #     )

    def settings(self):
        try:
            self.hide()
            self.master.settings()
            logger.debug('settings')
        except Exception as e:
            logger.exception('%s', e)

    def use_new_map(self):
        try:
            new_map = {}
            if (self.func1['text'] != 'spare') and (self.id1['text'] != ''):
                new_map[self.id1['text']] = self.func1['text']
            if (self.func2['text'] != 'spare') and (self.id2['text'] != ''):
                new_map[self.id2['text']] = self.func2['text']
            if (self.func3['text'] != 'spare') and (self.id3['text'] != ''):
                new_map[self.id3['text']] = self.func3['text']

            
            # TODO: uncomment after testing.
            logger.debug('use_new_map: %s', new_map)
            # reinstate when ready to test



            # self.master.id_map = new_map
            # self.master.update_out(reschedule=False)
        except Exception as e:
            logger.exception('%s', e)

    def increase_s1(self):
        try:
            if self.id1['text'] != '':
                self.func1['text'] = self.get_new_function(1, self.func1['text'])
                self.use_new_map()
            else:
                self.func1['text'] = 'spare'
        except Exception as e:
            logger.exception('%s', e)

    def clear(self):
        try:
            if self.id1['text'] != '':
                self.func1['text'] = self.get_new_function(1, self.func1['text'])
                self.use_new_map()
            else:
                self.func1['text'] = 'spare'
        except Exception as e:
            logger.exception('%s', e)

    def write(self):
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

    def get_new_function(self, slot, current_text):
        return current_text

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

        self.temp1a.place(x=0, y=0, height=0, width=0)
        self.temp2a.place(x=0, y=0, height=0, width=0)
        self.temp3a.place(x=0, y=0, height=0, width=0)

        self.s1_minus.place(x=0, y=0, height=0, width=0)
        self.s1_plus.place(x=0, y=0, height=0, width=0)

        self.s2_minus.place(x=0, y=0, height=0, width=0)
        self.s2_plus.place(x=0, y=0, height=0, width=0)

        self.s3_minus.place(x=0, y=0, height=0, width=0)
        self.s3_plus.place(x=0, y=0, height=0, width=0)

        self.clear_saved.place(x=0, y=0, height=0, width=0)
        self.write_offsets.place(x=0, y=0, height=0, width=0)

        # self.back_button.place(x=0, y=0, height=0, width=0)

    def show(self):
        self.sensor_map = self.xd.get(paths.sensor_map)
        self.sensors_raw = self.xd.get(paths.sensors_raw)
        self.populate_widgets()

        self.id1.place(x=140, y=30, height=80, width=100)
        self.id2.place(x=140, y=90, height=80, width=100)
        self.id3.place(x=140, y=150, height=80, width=100)

        self.func1.place(x=250, y=50, height=40, width=170)
        self.func2.place(x=250, y=110, height=40, width=170)
        self.func3.place(x=250, y=170, height=40, width=170)

        self.temp1.place(x=440, y=30, height=80, width=100)
        self.temp2.place(x=440, y=90, height=80, width=100)
        self.temp3.place(x=440, y=150, height=80, width=100)

        self.temp1a.place(x=560, y=30, height=80, width=100)
        self.temp2a.place(x=560, y=90, height=80, width=100)
        self.temp3a.place(x=560, y=150, height=80, width=100)

        self.s1_plus.place(x=670, y=40, height=50, width=40)
        self.s2_plus.place(x=670, y=100, height=50, width=40)
        self.s3_plus.place(x=670, y=160, height=50, width=40)

        self.s1_minus.place(x=740, y=40, height=50, width=40)
        self.s2_minus.place(x=740, y=100, height=50, width=40)
        self.s3_minus.place(x=740, y=160, height=50, width=40)

        self.clear_saved.place(x=200, y=230, height=50, width=200)
        self.write_offsets.place(x=460, y=230, height=50, width=260)

        self.back_button.place(x=10, y=134, height=52, width=110)
