from abc import ABCMeta, abstractmethod

class AbstractEdge(metaclass=ABCMeta):
    def __init__(self, i):
        self.id = i
        self.calibration = None

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
    # returns a tuple [beg, end]
    def get_limit_switch_state(self):
        raise NotImplementedError()

    def get_forward_limit_switch_state(self):
        if self.calibration is None:
            raise Exception(
                "Must set calibration before calling for forward/backwards limit switch")
        ls_state = self.get_limit_switch_state()
        if self.calibration.polarity:
            return ls_state[0]
        else:
            return ls_state[1]

    def get_reverse_limit_switch_state(self):
        if self.calibration is None:
            raise Exception(
                "Must set calibration before calling for forward/backwards limit switch")
        ls_state = self.get_limit_switch_state()
        if self.calibration.polarity:
            return ls_state[1]
        else:
            return ls_state[0]

    @abstractmethod
    def calibrate(self):
        raise NotImplementedError()
