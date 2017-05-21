from threading import Thread
from time import sleep, time

from torch_song.torch_song import AbstractEdge
from torch_song.motor_driver import MotorDriver
from torch_song.igniter import Igniter
from torch_song.valve import Valve
from torch_song.limit_switch import LimitSwitch

class RealEdge(AbstractEdge):

    def __init__(self, i, io, config, update_rate_hz = 100):
        super().__init__(i)
        self.motor_driver = MotorDriver(io['pca9685'],
                                        config['subsystems']['motors'][self.id - 1]['pwm_io'],
                                        config['subsystems']['motors'][self.id - 1]['dir_io'],
                                        config['subsystems']['motors'][self.id - 1]['dir_io_type'])
        beg_mcp_id = config['subsystems']['limit_switches'][self.id - 1]['beg_mcp_id']
        beg_mcp_io = config['subsystems']['limit_switches'][self.id - 1]['beg_mcp_io']
        end_mcp_id = config['subsystems']['limit_switches'][self.id - 1]['end_mcp_id']
        end_mcp_io = config['subsystems']['limit_switches'][self.id - 1]['end_mcp_io']
        self.limit_switch_beg = LimitSwitch(io['mcp23017'][beg_mcp_id], beg_mcp_io)
        self.limit_switch_end = LimitSwitch(io['mcp23017'][end_mcp_id], end_mcp_io)
        self.valve = Valve(config['subsystems']['valves'][self.id - 1]['gpio'])
        self.igniter = Igniter(config['subsystems']['igniters'][self.id - 1]['gpio'])

        self.speed_request = -1
        self.dir_request = MotorDriver.FORWARD

        self.update_rate_hz = update_rate_hz

        self.runner = Thread(target = self.loop)
        self.runner.setDaemon(True)
        self.runner.start()

    def __str__(self):
        s = "igniter: %d, valve: %d, beg. limit: %d, end. limit: %d, motor speed: %f, motor dir: %d" % (
                self.igniter.get_state(), self.valve.get_state(), self.limit_switch_beg.get_state(),
                self.limit_switch_end.get_state(), self.motor_driver.get_speed(),
                self.motor_driver.get_dir())
        return s

    def loop(self):
        self.pleaseExit = False
        while (not self.pleaseExit):
            now = time()
            # print('dir: %d beg: %d end %d' % (self.motor_driver.get_dir(), self.limit_switch_beg.get_state(), self.limit_switch_end.get_state())
            if (self.motor_driver.get_dir() == MotorDriver.FORWARD and
                    self.motor_driver.get_speed() > 0 and
                    self.limit_switch_end.get_state() == True):
                self.motor_driver.stop()
                print('End limit switch hit for id:%d' % self.id)
            elif (self.motor_driver.get_dir() == MotorDriver.REVERSE and
                    self.motor_driver.get_speed() > 0 and
                    self.limit_switch_beg.get_state() == True):
                self.motor_driver.stop()
                print('Beg limit switch hit for id:%d' % self.id)
            else:
                if (self.speed_request > 0):
                    self.motor_driver.set_speed(self.speed_request)
                    self.motor_driver.set_dir(self.dir_request)
                    self.speed_request = -1

            tosleep = 1.0/self.update_rate_hz - (now - time())
            if (tosleep > 0):
                sleep(tosleep)
            else:
                print('edge not calling sleep(), something weird is going on')

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

