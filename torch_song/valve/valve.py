from torch_song.relay import Relay

class Valve:
    OPEN = 0
    CLOSED = 1

    def __init__(self, pin):
        self.relay = Relay(pin);
        self.set_state(Valve.OPEN)

    def get_state(self):
        return self.relay.get_state()

    def set_state(self, state):
        if state not in [Valve.CLOSED, Valve.OPEN]:
            raise Exception("Invalid value for set_state")
        self.relay.set_state(state)

    def __del__(self):
        self.relay.set_state(Valve.OPEN)
