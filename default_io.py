#!/usr/bin/env python

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import yaml

stream = open('conf/default.yml', 'r')
config = yaml.load(stream)

from torch_song.igniter import Igniter
from torch_song.valve import Valve
from torch_song.motor_driver import MotorDriver
from torch_song.pca9685 import PCA9685

print('setting IO to off-state')

for v in config['subsystems']['igniters']:
    igniter = Igniter(v['gpio'])
    igniter.set_state(0)

for v in config['subsystems']['valves']:
    valve = Valve(v['gpio'])
    valve.set_state(0)

for m in config['subsystems']['motors']:
    motor = MotorDriver(PCA9685(), m['pwm_io'], m['dir_io'], m['dir_io_type'])
    motor.stop()
