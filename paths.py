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

beer_temp = 'beer_temp'
beer_target = 'beer_target'
chamber_temp = 'chamber_temp'
blue_sg = 'blue_sg'

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

action_settings = 'Settings'
action_back = 'Back'

sensor_map = 'sensor_map'
relays_ts = 'relays_ts'
desired_ts = 'desired_ts'

sensors_raw = 'sensors_raw'
