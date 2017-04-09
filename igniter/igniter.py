from relay import Relay

class Igniter:
    OFF = 0
    ON = 1

    def __init__(self, io):
        self._relay = Relay(io);
        self.set_state(Igniter.OFF)

    def get_state(self):
        return self._relay.get_state()

    def set_state(self, state):
        if state not in [Igniter.ON, Igniter.OFF]:
            raise Exception("Invalid value for set_state")
        self._relay.set_state(state)

    def __del__(self):
        self._relay.set_state(Igniter.OFF)
