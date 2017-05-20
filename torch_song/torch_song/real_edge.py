from threading import Thread
from time import sleep

from torch_song.torch_song import AbstractEdge
from torch_song.motor_driver import MotorDriver
from torch_song.igniter import Igniter
from torch_song.valve import Valve
from torch_song.limit_switch import LimitSwitch

class RealEdge(AbstractEdge):

    def __init__(self, i, io, config):
        super().__init__(i)
        self.motor_driver = MotorDriver(io['pca9685'],
                                        config['subsystems']['motors'][self.id]['pwm_io'],
                                        config['subsystems']['motors'][self.id]['dir_io'],
                                        config['subsystems']['motors'][self.id]['dir_io_type'])
        beg_mcp_id = config['subsystems']['limit_switches'][self.id]['beg_mcp_id']
        beg_mcp_io = config['subsystems']['limit_switches'][self.id]['beg_mcp_io']
        end_mcp_id = config['subsystems']['limit_switches'][self.id]['end_mcp_id']
        end_mcp_io = config['subsystems']['limit_switches'][self.id]['end_mcp_io']
        self.limit_switch_beg = LimitSwitch(io['mcp23017'][beg_mcp_id], beg_mcp_io)
        self.limit_switch_end = LimitSwitch(io['mcp23017'][end_mcp_id], end_mcp_io)
        self.valve = Valve(config['subsystems']['valves'][self.id]['gpio'])
        self.igniter = Igniter(config['subsystems']['igniters'][self.id]['gpio'])

        self.speed_request = 0
        self.last_speed_request = self.speed_request
        self.dir_request = MotorDriver.FORWARD
        self.last_dir_request = self.dir_request

        self.runner = Thread(target = self.loop)
        self.runner.setDaemon(True)
        self.runner.start()

    def loop(self):
        self.pleaseExit = False
        while (not self.pleaseExit):
            if (MotorDriver.get_dir == MotorDriver.FORWARD and self.limit_switch_end.get_state() == True):
                self.motor_driver.stop()
            elif (MotorDriver.get_dir == MotorDriver.REVERSE and self.limit_switch_beg.get_state() == True):
                self.motor_driver.stop()
            elif (self.speed_request != self.last_speed_request):
                self.motor_driver.set_speed(self.speed_request)

            if (self.dir_request != self.last_dir_request):
                self.motor_driver.set_dir(self.dir_request)

            self.last_dir_request = self.dir_request
            self.last_speed_request = self.speed_request
            sleep(.01)

    def set_motor_state(self, direction, speed):
        self.dir_request = direction
        self.speed_request = speed

    def set_valve_state(self, v):
        self.valve.set_state(v)

    def set_igniter_state(self, g):
        self.igniter.set_state(g)

    def get_limit_switch_state(self):
        return [self.limit_switch_beg.get_state(), self.limit_switch_end.get_state()]

    def calibrate(self):
        pass

    def __del__(self):
        self.pleaseExit = True
        self.runner.join(5000)

