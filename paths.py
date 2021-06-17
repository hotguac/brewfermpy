#!/usr/bin/python3

base = '/home/pi/brewferm/'
logs = base + 'logs/brewferm.log'
xchg = base + 'xchg/'
resources = base + 'resources/'

sensors_out = xchg + 'sensors_out.mmap'
controller_out = xchg + 'controller_out.mmap'
relays_out = xchg + 'relays_out.mmap'
gui_out = xchg + 'gui_out.mmap'

#gui_in = xchg + 'gui_in.mmap'

beerPID = 'beerPID'
chamberPID = 'chamberPID'

current = "current"
desired = "desired"

beer_temp = "beer_temp"
beer_target = "beer_target"
chamber_temp = "chamber_temp"

idle = "Idle"
cool = "Cool"
heat = "Heat"

state = "state"
running = "running"
paused = "paused"
