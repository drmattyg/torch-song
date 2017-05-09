from abc import ABCMeta, abstractmethod


class AbstractEdge(metaclass=ABCMeta):
    def __init__(self, i):
        self.id = i

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
    def get_limit_switch_state(self):
        raise NotImplementedError()
