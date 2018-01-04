class LimitSwitch:
    def __init__(self, mcp, io):
        self.mcp = mcp
        self.io = io

    def get_state(self):
        return not self.mcp.get_state()[self.io]


class DebounceLimitSwitch(LimitSwitch):
    def __init__(self, mcp, io, debounce_state=True, debounce_count=3):
        super().__init__(mcp, io)
        self.debounce_state = debounce_state
        self.debounce_count = debounce_count
        self.last_state = None
        self.state_count = 0

    def get_state(self):
        state = super(DebounceLimitSwitch, self).get_state()

        # if False, just return False
        if state != self.debounce_state:
            self.last_state = state
            return state

        # if this wasn't our state last time, reset the state counter
        if state != self.last_state:
            self.state_count = 0

        # increment the state counter and set the last_state
        self.state_count += 1
        self.last_state = state

        # if we've exceeded the state counter, reset the state counter and return the state
        if self.state_count > self.debounce_count:
            self.state_count = 0
            return state

        # otherwise, return the default state
        else:
            return not state
