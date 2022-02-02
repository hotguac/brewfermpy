#!/usr/bin/python3

# Import 3rd party libraries ----------------------------------------
import tkinter as tk
import tkinter.font as font

# Import standard libraries -----------------------------------------
import logging

# Import application libraries --------------------------------------
import assign
import beer_temps
import colors
import paths
import settings

from xchg import XchgData


# ------------------------------------------------
# Middle section of screen
# ------------------------------------------------
class gMiddle(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.btemps = None  # will hold a gBeerTemps object
        self.menu = None  # will hold a gMenu object
        self.sensor_assign = None  # will hold a gAssign object

        self.xd = XchgData(paths.gui_out)

        self.beer_temp = self.xd.get(paths.beer_temp, 69.0)

        # This will set the default if no gui_out.mmap exists !!!!
        self.beer_target = self.xd.get(paths.beer_target, 75.0)
        self.state = self.xd.get(paths.state, paths.running)

        btuning = self.xd.get(paths.beerPID, {})

        self.beer_kp = btuning.get('kp', 8.0)
        self.beer_ki = btuning.get('ki', 0.0015)  # 0.0001
        self.beer_kd = btuning.get('kd', 0.0)
        self.beer_sample_time = btuning.get('sample_time', 60)

        ctuning = self.xd.get(paths.chamberPID, {})

        self.chamber_kp = ctuning.get('kp', 6.0)  # 6.0
        self.chamber_ki = ctuning.get('ki', 0.004)  # 0.004
        self.chamber_kd = ctuning.get('kd', 0.0)
        self.chamber_sample_time = ctuning.get('sample_time', 15)

        self.relays_off_on = 6  # minutes - minimum of 6 for safety
        self.relays_max_on = 6  # minutes
        self.relays_hc_balance = 2.0
        self.relays_zone_size = 20  # 0-20 cool ; 80-100 heat

        temp_map = {  # TODO: user configure
            '28-00000b812382': 'beer',
            '28-000008802d75': 'chamber'
        }

        self.id_map = self.xd.get(paths.sensor_map, temp_map)

        self.create_widgets()
        self.after(1000, self.update_out)

    def create_widgets(self):
        self.values_box = tk.Frame(self.master)
        self.values_box['bg'] = colors.background
        self.values_box.place(x=0, y=40, height=320, width=800)

        self.title_box = tk.Frame(self.values_box)
        self.title_box.place(x=160, y=0, height=40, width=640)
        self.title_box['bg'] = colors.background

        self.button_box = tk.Frame(self.values_box)
        self.button_box['bg'] = colors.background
        self.button_box.place(x=0, y=0, height=320, width=160)

        self.image_tc = tk.PhotoImage(file=paths.resources + "top_corner.png")
        self.top_corner = tk.Label(self.button_box, image=self.image_tc)
        self.top_corner.place(x=0, y=0, width=160, height=60)

        self.image_bc = tk.PhotoImage(
            file=paths.resources + "bottom_corner.png")
        self.bottom_corner = tk.Label(self.button_box, image=self.image_bc)
        self.bottom_corner.place(x=0, y=260, width=160, height=60)

        self.button_font = font.Font(family="Arial", size=-18, weight="normal")

        self.pause_button = tk.Button(
            self.button_box,
            text="Pause",
            command=self.pause_brew,
            bg=colors.normal_button,
            font=self.button_font,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.pause_button.place(x=10, y=70, height=52, width=110)

        self.settings_button = tk.Button(
            self.button_box,
            text="Settings",
            command=self.settings,
            background=colors.normal_button,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.settings_button.place(x=10, y=134, height=52, width=110)

        self.exit_button = tk.Button(
            self.button_box,
            text="Exit",
            command=self.exit_brew,
            background=colors.normal_button,
            borderwidth=0,
            highlightthickness=0,
            font=self.button_font,
            activebackground=colors.normal_button,
            highlightbackground=colors.normal_button,
            highlightcolor=colors.normal_button,
            relief=tk.FLAT
            )

        self.exit_button.place(x=10, y=198, height=52, width=110)

        self.image_bb = tk.PhotoImage(file=paths.resources + "bottom_bar.png")
        self.bottom_bar = tk.Label(self.values_box, image=self.image_bb)
        self.bottom_bar.place(x=160, y=280, width=640, height=40)

        self.image_tb = tk.PhotoImage(file=paths.resources + "top_bar.png")
        self.top_bar = tk.Label(self.values_box, image=self.image_tb)
        self.top_bar.place(x=160, y=0, width=640, height=40)

        self.lbl_current = tk.Label(
            self.values_box,
            text="Temp F",
            bg=colors.background,
            fg=colors.invert_text,
            font=("Arial", -24)
            )

        self.lbl_current.place(x=220, y=0, height=40, width=160)

        self.lbl_target = tk.Label(self.values_box, text="Target F")
        self.lbl_target["bg"] = colors.background
        self.lbl_target["fg"] = colors.invert_text
        self.lbl_target["font"] = ("Arial", -24)
        self.lbl_target.place(x=580, y=0, height=40, width=160)

    def update_out(self):
        try:
            self.after(500, self.update_out)

            if self.btemps is None:
                self.btemps = beer_temps.gBeerTemps(master=self)
                self.btemps.show_beer()

            if self.menu is None:
                self.menu = settings.gMenu(master=self)

            if self.sensor_assign is None:
                self.sensor_assign = assign.gAssign(master=self)

            self.xd.write_gui(self.format_state())
        except Exception as e:
            logging.exception('%s %s', type(e), e)

    def format_state(self):
        x = {}
        x[paths.beer_target] = self.beer_target
        x[paths.state] = self.state

        x['beer_pid'] = {
            'kp': self.beer_kp,
            'ki': self.beer_ki,
            'kd': self.beer_kd,
            'sample_time': self.beer_sample_time
            }

        x['chamber_pid'] = {
            'kp': self.chamber_kp,
            'ki': self.chamber_ki,
            'kd': self.chamber_kd,
            'sample_time': self.chamber_sample_time
            }

        x['relays'] = {
            'off_on': self.relays_off_on,
            'max_on': self.relays_max_on,
            'hc_balance': self.relays_hc_balance,
            'zone_size': self.relays_zone_size
        }

        x['id_map'] = self.id_map
        # {  # TODO: user configure
        #     '28-00000b812382': 'beer',
        #     '28-000008802d75': 'chamber'
        # }

        return x

    def pause_brew(self):
        try:
            if self.pause_button['text'] == "Pause":
                logging.warning("brewing paused...")
                self.state = paths.paused
                self.pause_button['text'] = "Resume"
            else:
                logging.info("brewing resumed...")
                self.pause_button['text'] = "Pause"
                self.state = paths.running

        except Exception as e:
            logging.exception(e)

    def exit_brew(self):
        logging.info("exiting gui")
        self.master.destroy()

    def settings(self):
        try:
            if self.settings_button['text'] == paths.action_settings:
                self.settings_button['text'] = paths.action_back
                self.btemps.hide()
                self.menu.show()
            else:
                if self.settings_button['text'] == paths.action_back:
                    self.settings_button['text'] = paths.action_settings
                    self.menu.hide()
                    self.sensor_assign.hide()
                    self.btemps.show_beer()

        except Exception as e:
            logging.exception("settings %s %s", type(e), e)
