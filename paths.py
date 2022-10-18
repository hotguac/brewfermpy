#!/usr/bin/python3

base = '/home/pi/brewferm/'
logs = base + 'logs/brewferm.log'
xchg = base + 'xchg/'
resources = base + 'resources/'

sensors_out = xchg + 'sensors_out.mmap'
controller_out = xchg + 'controller_out.mmap'
relays_out = xchg + 'relays_out.mmap'
gui_out = xchg + 'gui_out.mmap'
blue_out = xchg + 'blue_out.mmap'

beerPID = 'beerPID'
chamberPID = 'chamberPID'

current = 'current'
desired = 'desired'

ambient_temp = 'ambient_temp'
beer_temp = 'beer_temp'
beer_target = 'beer_target'
chamber_temp = 'chamber_temp'
blue_sg = 'blue_sg'
blue_ts = 'blue_ts'

idle = 'Idle'
cool = 'Cool'
heat = 'Heat'

state = 'state'
running = 'running'
paused = 'paused'

default_beer_target = 64

beer_sensor = 'Beer'
chamber_sensor = 'Chamber'
ambient_sensor = 'Ambient'
spare_sensor = 'Spare'

action_menu = 'Menu'
action_back = 'Back'

sensor_map = 'sensor_map'
relays_ts = 'relays_ts'
desired_ts = 'desired_ts'

sensors_raw = 'sensors_raw'

default_beerP = 8.0
default_beerI = 0.003 # 0.0015
default_beerD = 0

default_chamberP = 6.0
default_chamberI = 0.004
default_chamberD = 0
