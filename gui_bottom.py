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

        self.xd = XchgData()  # we only need read in the bottom

        self.create_widgets()
        self.update_input()

    def update_input(self):
        try:
            self.master.after(2000, self.update_input)

            temp = self.xd.get(paths.chamber_temp, 0.0) + self.xd.get(paths.chamber_temp_offset, 0.0)

            self.chamber_temp['text'] = round(temp)

            x = self.xd.get(paths.desired)
            self.desired_state['text'] = x
            if x == 'Idle':
                self.desired_state["fg"] = colors.normal50
            else:
                if x == 'Cool':
                    self.desired_state["fg"] = colors.cool200
                else:
                    self.desired_state["fg"] = colors.warm400

            x = self.xd.get(paths.current)
            self.current_state['text'] = x
            if x == 'Idle':
                self.current_state["fg"] = colors.normal50
            else:
                if x == 'Cool':
                    self.current_state["fg"] = colors.cool200
                else:
                    self.current_state["fg"] = colors.warm400

        except Exception as e:
            logger.exception('%s %s', type(e), e)

    def create_widgets(self):
        #
        #       Heat/Cool Section (bottom)
        #
        self.image_tb = tk.PhotoImage(file=paths.resources + "top_bar.png")
        self.image_tc = tk.PhotoImage(file=paths.resources + "top_corner.png")
        self.image_lm = tk.PhotoImage(
            file=paths.resources + "bottom_bottom.png")

        self.heatcool = tk.Frame(self.master)
        self.heatcool["bg"] = colors.background

        self.current_state = tk.Label(self.heatcool, text=paths.idle)
        self.current_state["bg"] = colors.background
        self.current_state["fg"] = colors.normal50
        self.current_state["font"] = ("Arial", -60)

        self.chamber_temp = tk.Label(self.heatcool, text="99.9")
        self.chamber_temp["bg"] = colors.background
        self.chamber_temp["fg"] = colors.normal400
        self.chamber_temp["font"] = ("Arial", -40)

        self.desired_state = tk.Label(self.heatcool, text="Cool")
        self.desired_state["bg"] = colors.background
        self.desired_state["fg"] = colors.cool200
        self.desired_state["font"] = ("Arial", -40)

        self.side_bar = tk.Frame(self.heatcool)
        self.side_bar['bg'] = colors.background

        self.top_corner = tk.Label(self.side_bar, image=self.image_tc)
        self.left_middle = tk.Label(self.side_bar, image=self.image_lm)

        self.title_bar = tk.Frame(self.heatcool)
        self.title_bar['bg'] = colors.background

        self.top_bar = tk.Label(self.title_bar, image=self.image_tb)

        self.target = tk.Label(self.title_bar, text="Desired")
        self.target["bg"] = self.title_bar["bg"]
        self.target["fg"] = colors.invert_text
        self.target["font"] = ("Arial", -24)

        self.running = tk.Label(self.title_bar, text="Now")
        self.running["bg"] = colors.background
        self.running["fg"] = colors.invert_text
        self.running["font"] = ("Arial", -24)

        self.lbl_chamber = tk.Label(self.title_bar, text="Chamber F")
        self.lbl_chamber["bg"] = colors.background
        self.lbl_chamber["fg"] = colors.invert_text
        self.lbl_chamber["font"] = ("Arial", -16)

        self.heatcool.place(x=0, y=360, height=120, width=800)

        self.current_state.place(x=160, y=40, height=80, width=220)
        self.chamber_temp.place(x=430, y=40, height=80, width=80)
        self.desired_state.place(x=580, y=40, height=80, width=160)

        self.side_bar.place(x=0, y=0, height=120, width=160)
        # relative to side_bar
        self.top_corner.place(x=0, y=0, width=160, height=60)
        self.left_middle.place(x=0, y=60, width=160, height=60)

        self.title_bar.place(x=160, y=0, height=40, width=640)
        # relative to title bar
        self.top_bar.place(x=0, y=0, width=640, height=40)
        self.running.place(x=50, y=0, height=40, width=100)
        self.lbl_chamber.place(x=260, y=0, height=40, width=110)
        self.target.place(x=440, y=0, height=40, width=120)
