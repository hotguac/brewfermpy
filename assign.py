#!/usr/bin/python3

# Import 3rd party libraries ----------------------------------------
import tkinter as tk
import tkinter.font as font
# import tkFont

# Import standard libraries -----------------------------------------
import logging

# Import application libraries --------------------------------------
import colors

from xchg import XchgData


# -------------------------------------------------------------------
#  Associate attached sensors to beer, chamber, or ambient temps
# -------------------------------------------------------------------
class gAssign(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.xd = XchgData()  # read only for now

        self.create_widgets()
        self.update_ok()

    def create_widgets(self):
        # normal_font = font.Font(family='FreeMono', size=-36)  # , weight='bold')
        normal_font = font.Font(family='DejaVu Sans Mono', size=-36)  # , weight='bold')

        self.id1 = tk.Label(self.master.values_box,
                            text="28-00000b812382",
                            background=colors.background,
                            fg=colors.normal50,
                            anchor='w',
                            font=normal_font
                            )

        self.id2 = tk.Label(self.master.values_box,
                            text="28-000008802d75",
                            background=colors.background,
                            fg=colors.normal50,
                            anchor='w',
                            font=normal_font
                            )

        self.id3 = tk.Label(self.master.values_box,
                            text="28-00000ff00fff",
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
                              text="63",
                              background=colors.background,
                              fg=colors.normal50,
                              anchor='w',
                              font=normal_font
                              )

        self.button_font = font.Font(family="Arial", size=-32, weight="bold")

        self.func1 = tk.Button(
            self.master.values_box,
            text="Beer",
            command=self.store,
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
            text="Chamber",
            command=self.store,
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
            text="Unknown",
            command=self.store,
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

        self.ok = tk.Button(
            self.master.values_box,
            text="ok",
            command=self.store,
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
            logging.exception("%s %s", type(e), e)

    def store(self):
        logging.debug('in assign store')

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

        self.ok.place(x=0, y=0, height=0, width=0)

    def show(self):
        self.id1.place(x=140, y=60, height=80, width=340)
        self.id2.place(x=140, y=120, height=80, width=340)
        self.id3.place(x=140, y=180, height=80, width=340)

        self.func1.place(x=500, y=80, height=40, width=220)
        self.func2.place(x=500, y=140, height=40, width=220)
        self.func3.place(x=500, y=200, height=40, width=220)

        self.temp1.place(x=740, y=60, height=80, width=80)
        self.temp2.place(x=740, y=120, height=80, width=80)
        self.temp3.place(x=740, y=180, height=80, width=80)
