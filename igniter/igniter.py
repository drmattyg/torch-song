from relay import Relay

class Igniter:
    OPEN = 0
    CLOSED = 1

    def __init__(self, io):
        self._relay = Relay(io);
        self.set_state(Igniter.OPEN)

    def get_state(self):
        return self._relay.get_state()

    def set_state(self, state):
        if state not in [Igniter.CLOSED, Igniter.OPEN]:
            raise Exception("Invalid value for set_state")
        self._relay.set_state(state)

    def __del__(self):
        self._relay.set_state(Igniter.OPEN)
