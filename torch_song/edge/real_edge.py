from threading import Thread, Lock
from time import sleep, time
import logging

from torch_song.calibration import EdgeCalibration
from torch_song.common import try_decorator
from torch_song.edge import AbstractEdge
from torch_song.hardware.motor_driver import MotorDriver
from torch_song.hardware.igniter import Igniter
from torch_song.hardware.valve import Valve
from torch_song.hardware.limit_switch import LimitSwitch


class RealEdge(AbstractEdge):
    def __init__(self, i, io, config, update_rate_hz=20, calibration=None):
        super().__init__(i)

        # Hardware config
        self.motor_driver = MotorDriver(io['pca9685'],
                                        config['subsystems']['motors'][self.id - 1]['pwm_io'],
                                        config['subsystems']['motors'][self.id - 1]['dir_io'],
                                        config['subsystems']['motors'][self.id - 1]['dir_io_type'],
                                        config['subsystems']['motors'][self.id - 1]['polarity'])
        beg_mcp_id = config['subsystems']['limit_switches'][self.id - 1]['beg_mcp_id']
        beg_mcp_io = config['subsystems']['limit_switches'][self.id - 1]['beg_mcp_io']
        end_mcp_id = config['subsystems']['limit_switches'][self.id - 1]['end_mcp_id']
        end_mcp_io = config['subsystems']['limit_switches'][self.id - 1]['end_mcp_io']
        self.limit_switch_beg = LimitSwitch(io['mcp23017'][beg_mcp_id], beg_mcp_io)
        self.limit_switch_end = LimitSwitch(io['mcp23017'][end_mcp_id], end_mcp_io)
        self.valve = Valve(config['subsystems']['valves'][self.id - 1]['gpio'])
        self.igniter = Igniter(config['subsystems']['igniters'][self.id - 1]['gpio'])
        self.dir_polarity =  config['subsystems']['motors'][self.id - 1]['polarity']

        self.position = 0

        # Thread daemon inits
        self.speed_request = -1
        self.dir_request = 0
        self._ignore_limit = False
        self.update_rate_hz = update_rate_hz

        # Safety params
        self.time_of_last_limit_switch = time()
        self.STALL_TIME = 10

        if calibration is None:
            # insert a default calibration
            self.set_calibration(EdgeCalibration(self))

        # let limit switches settle
        try_decorator(timeout=5)(lambda:not all(self.get_limit_switch_state()))()

        # Threading
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

        last_cal_time = 0
        prev_time = time()

        while (not self.pleaseExit):
            self.lock.acquire()
            now = time()

            if (not last_cal_time == 0):
                self.position += (now - prev_time) / last_cal_time

            prev_time = now

            #safety checks  
            #both limit switches on
            if all(self.get_limit_switch_state()):
                raise Exception('Both limit switches on for edge', self.id)

            #stalled motor
            if (any(self.get_limit_switch_state()) or self.motor_driver.get_speed() == 0):
                self.time_of_last_limit_switch = time()
            if (self.motor_driver.get_speed() > 0 and
                time()-self.time_of_last_limit_switch > self.STALL_TIME):
                pass
                #raise Exception('Stalled motor')

            self.motor_driver.set_dir(MotorDriver.REVERSE if self.dir_request == -1 else MotorDriver.FORWARD)

            if (self.motor_driver.get_dir() == MotorDriver.FORWARD and
                        self.motor_driver.get_speed() > 0 and
                        not self._ignore_limit and
                        self.get_forward_limit_switch_state() == True):
                self.motor_driver.stop()
                self.speed_request = 0
                self.position = 1
                last_cal_time = 0
                logging.info('Fwd limit switch hit for id:%d' % (self.id), extra={'edge_id': self.id})
            elif (self.motor_driver.get_dir() == MotorDriver.REVERSE and
                        self.motor_driver.get_speed() > 0 and
                        not self._ignore_limit and
                        self.get_reverse_limit_switch_state() == True):
                self.motor_driver.stop()
                self.speed_request = 0
                self.position = 0
                last_cal_time = 0
                logging.info('Rev limit switch hit for id:%d' % (self.id), extra={'edge_id': self.id})
            elif (self.speed_request >= 0):
                    self.motor_driver.set_speed(self.speed_request)
                    self.speed_request = -1
                    last_cal_time = self.calibration.get_cal_time(self.speed_request, self.dir_request)
                    last_cal_time = last_cal_time * self.dir_request
            else:
                last_cal_time = 0

            self.lock.release()

            tosleep = 1.0 / self.update_rate_hz - (time() - now)
            if (tosleep > 0):
                sleep(tosleep)
            else:
                print('edge not calling sleep(), something weird is going on')

    def _ignore_limit_switch(self, state):
        self.lock.acquire()
        self._ignore_limit = state
        self.lock.release()

    def set_motor_state(self, direction, speed):
        self.lock.acquire()
        self.dir_request = direction
        self.speed_request = speed
        logging.info('id:%d speed:%d dir:%d' % (self.id, speed, direction), extra={'edge_id': self.id})
        self.lock.release()

    def set_valve_state(self, v):
        self.valve.set_state(v)

    def set_igniter_state(self, g):
        self.igniter.set_state(g)

    def get_limit_switch_state(self):
        return [self.limit_switch_beg.get_state(), self.limit_switch_end.get_state()]

    def at_limit(self):
        return self.limit_switch_beg.get_state() or self.limit_switch_end.get_state()

    def move_to_start(self):
        self.set_motor_state(-1, 75);

    def calibrate(self):
        self._ignore_limit_switch(True)
        self.calibration.calibrate()
        self._ignore_limit_switch(False)

    def get_position(self):
        return self.position

    def get_valve_state(self):
        return self.valve.get_state()

    def get_igniter_state(self):
        return self.igniter.get_state()


    def get_calibration(self):
        return self.calibration

    def kill(self):
        self.motor_driver.stop()
        self.pleaseExit = True
        self.runner.join(5000)

    def __del__(self):
        self.kill()
