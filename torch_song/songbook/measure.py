from collections import namedtuple


class Measure:
    IGNITER = "I"
    MOTOR = "M"
    VALVE = "V"
    Transition = namedtuple("Transition", ["type", "id", "value"])
    MotorState = namedtuple("MotorState", ["direction", "speed"])

    def __init__(self, start_time, run_time):
        self.start_time = start_time
        self.run_time = run_time
        self.edge_states = []

    def add_transition(self, tx):
        self.edge_states.append(tx)
