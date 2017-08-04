from abc import ABCMeta, abstractmethod

from torch_song.calibration import EdgeCalibration
from torch_song.common import try_decorator
import time
import logging


class AbstractEdge(metaclass=ABCMeta):
    def __init__(self, i):
        self.id = i
        self.calibration = EdgeCalibration(self)

    def set_calibration(self, calibration):
        self.calibration = calibration

    @abstractmethod
    def set_motor_state(self, direction, speed):
        raise NotImplementedError()

    @abstractmethod
    def set_valve_state(self, v):
        raise NotImplementedError()

    @abstractmethod
    def set_igniter_state(self, g):
        raise NotImplementedError()

    @abstractmethod
    def get_valve_state(self):
        raise NotImplementedError()

    @abstractmethod
    def get_igniter_state(self):
        raise NotImplementedError()

    @abstractmethod
    # returns an uncalibrated tuple [beg, end] of limit switches
    def get_limit_switch_state(self):
        raise NotImplementedError()

    def get_forward_limit_switch_state(self):
        if self.get_calibration() is None:
            raise Exception(
                "Must set calibration before calling for forward/backwards limit switch")
        ls_state = self.get_limit_switch_state()
        if self.get_calibration().polarity:
            return ls_state[0]
        else:
            return ls_state[1]

    def get_reverse_limit_switch_state(self):
        if self.get_calibration() is None:
            raise Exception(
                "Must set calibration before calling for forward/backwards limit switch")
        ls_state = self.get_limit_switch_state()
        if self.get_calibration().polarity:
            return ls_state[1]
        else:
            return ls_state[0]

    @abstractmethod
    def calibrate(self):
        raise NotImplementedError()

    def home(self):
        self.set_igniter_state(0)
        self.set_valve_state(0)
        if (self.get_reverse_limit_switch_state()):
            return True

        self.set_motor_state(-1, 90)
        func = try_decorator(15)(self.get_reverse_limit_switch_state)
        result = func()
        if result is False:
            raise Exception('Failed to home on id:' + str(self.id))
        return result

    def go_middle(self):
        self.home()
        duty_cycle = 80
        sleep_time = self.get_calibration().get_cal_time(duty_cycle, 1)
        self.set_motor_state(1, duty_cycle)
        time.sleep(sleep_time / 2)
        self.set_motor_state(1, 0)

    @abstractmethod
    def get_position(self):
        raise NotImplementedError()

    @abstractmethod
    def kill(self):
        raise NotImplementedError()

    @abstractmethod
    def get_calibration(self):
        raise NotImplementedError()

    @abstractmethod
    def is_healthy(self):
        raise NotImplementedError()
