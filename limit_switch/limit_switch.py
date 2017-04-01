class LimitSwitch:

    def __init__(self, mcp, io):
        self.mcp = mcp
        self.io = io

    def get_state(self, update=True):
        if update:
            self.mcp.update()
        return self.mcp.state[self.io]
