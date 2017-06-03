from threading import Thread, Lock
from time import sleep, time

from torch_song.calibration import EdgeCalibration
from torch_song.edge import AbstractEdge
from torch_song.hardware import MotorDriver
from torch_song.hardware import Igniter
from torch_song.hardware import Valve
from torch_song.hardware import LimitSwitch


class RealEdge(AbstractEdge):
    def __init__(self, i, io, config, update_rate_hz=100, calibration=None):
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

        if calibration is None:
            # insert a default calibration
            self.set_calibration(EdgeCalibration(self))

        self.lock = Lock()

        self.runner = Thread(target=self.loop)
        self.runner.setDaemon(True)
        self.runner.start()

    def __str__(self):
        s = "igniter: %d, valve: %d, beg. limit: %d, end. limit: %d, motor speed: %f, motor dir: %s" % (
            self.igniter.get_state(), self.valve.get_state(), self.limit_switch_beg.get_state(),
            self.limit_switch_end.get_state(), self.motor_driver.get_speed(),
            self.motor_driver.get_dir_str())
        return s

    def loop(self):
        self.pleaseExit = False
        while (not self.pleaseExit):
            self.lock.acquire()
            now = time()
            # print('dir: %d beg: %d end %d' % (self.motor_driver.get_dir(), self.limit_switch_beg.get_state(), self.limit_switch_end.get_state())
            if (self.motor_driver.get_dir() == MotorDriver.FORWARD and
                        self.motor_driver.get_speed() > 0 and
                        self.get_forward_limit_switch_state() == True):
                self.motor_driver.stop()
                self.speed_request = 0
                print('End limit switch hit for id:%d' % self.id)
            elif (self.motor_driver.get_dir() == MotorDriver.REVERSE and
                          self.motor_driver.get_speed() > 0 and
                          self.get_reverse_limit_switch_state() == True):
                self.motor_driver.stop()
                self.speed_request = 0
                print('Beg limit switch hit for id:%d' % self.id)
            else:
                if (self.speed_request >= 0):
                    self.motor_driver.set_speed(self.speed_request)
                    self.motor_driver.set_dir(self.dir_request)
                    self.speed_request = -1
            self.lock.release()

            tosleep = 1.0 / self.update_rate_hz - (now - time())
            if (tosleep > 0):
                sleep(tosleep)
            else:
                print('edge not calling sleep(), something weird is going on')

    def set_motor_state(self, direction, speed):
        self.lock.acquire()
        self.dir_request = direction
        self.speed_request = speed
        self.lock.release()

    def set_valve_state(self, v):
        self.valve.set_state(v)

    def set_igniter_state(self, g):
        self.igniter.set_state(g)

    def get_limit_switch_state(self):
        return [self.limit_switch_beg.get_state(), self.limit_switch_end.get_state()]

    def at_limit(self):
        return self.limit_switch_beg.get_state() or self.limit_switch_end.get_state()

    def calibrate(self):
        pass

    def __del__(self):
        self.motor_driver.stop()
        self.pleaseExit = True
        self.runner.join(5000)
