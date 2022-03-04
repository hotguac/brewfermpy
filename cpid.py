#!/usr/bin/python3

# Import 3rd party libraries ----------------------------------------
import tkinter as tk
import tkinter.font as font

# Import standard libraries -----------------------------------------

# Import application libraries --------------------------------------
import colors
import paths

from xchg import XchgData


# -------------------------------------------------------------------
#  Associate attached sensors to chamber, chamber, or ambient temps
# -------------------------------------------------------------------
class gCPID(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.create_widgets()

        self.xd = XchgData()  # read only for now

        self.visible = False
        self.populate_widgets()

    def populate_widgets(self):
        self.chamber_P['text'] = 'P ' + str(round(self.master.chamber_kp, 1))
        self.chamber_I['text'] = 'I ' + str(round(self.master.chamber_ki, 4))

    def create_widgets(self):
        font1 = font.Font(family='TkTextFont', size=-60, weight='bold')
        font2 = font.Font(family='TkTextFont', size=-40, weight='bold')

        self.plus_P = tk.Button(
            self.master.values_box,
            text="+",
            command=self.increase_P,
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=font1,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.minus_P = tk.Button(
            self.master.values_box,
            text="-",
            command=self.decrease_P,
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=font1,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.default_P = tk.Button(
            self.master.values_box,
            text="@",
            command=self.default_P,
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=font2,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.chamber_P = tk.Label(
            self.master.values_box,
            text="P ?.?",
            background=colors.background,
            fg=colors.normal50,
            font=font2
            )

        # Integrator Values

        self.plus_I = tk.Button(
            self.master.values_box,
            text="+",
            command=self.increase_I,
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=font1,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.minus_I = tk.Button(
            self.master.values_box,
            text="-",
            command=self.decrease_I,
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=font1,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.default_I = tk.Button(
            self.master.values_box,
            text="@",
            command=self.default_I,
            foreground=colors.background,
            background=colors.normal50,
            borderwidth=0,
            highlightthickness=0,
            font=font2,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.chamber_I = tk.Label(
            self.master.values_box,
            text="I ?.?",
            background=colors.background,
            fg=colors.normal50,
            font=font2
            )

    def increase_P(self):
        self.master.chamber_kp += 0.1
        self.populate_widgets()

    def decrease_P(self):
        self.master.chamber_kp -= 0.1
        self.populate_widgets()

    def default_P(self):
        self.master.chamber_kp = paths.default_chamberP
        self.populate_widgets()

    def increase_I(self):
        self.master.chamber_ki += 0.0005
        self.populate_widgets()

    def decrease_I(self):
        self.master.chamber_ki -= 0.0005
        self.populate_widgets()

    def default_I(self):
        self.master.chamber_ki = paths.default_chamberI
        self.populate_widgets()

    def hide(self):
        self.visible = False

        self.plus_P.place(x=0, y=0, height=0, width=0)
        self.minus_P.place(x=0, y=0, height=0, width=0)
        self.chamber_P.place(x=0, y=0, height=0, width=0)
        self.default_P.place(x=0, y=0, height=0, width=0)

        self.plus_I.place(x=0, y=0, height=0, width=0)
        self.minus_I.place(x=0, y=0, height=0, width=0)
        self.chamber_I.place(x=0, y=0, height=0, width=0)
        self.default_I.place(x=0, y=0, height=0, width=0)

    def show(self):
        self.visible = True
        self.populate_widgets()

        self.plus_P.place(x=160, y=60, height=60, width=60)
        self.minus_P.place(x=260, y=60, height=60, width=60)
        self.chamber_P.place(x=360, y=60, height=60, width=240)
        self.default_P.place(x=720, y=60, height=60, width=80)

        self.plus_I.place(x=160, y=140, height=60, width=60)
        self.minus_I.place(x=260, y=140, height=60, width=60)
        self.chamber_I.place(x=360, y=140, height=60, width=240)
        self.default_I.place(x=720, y=140, height=60, width=80)
