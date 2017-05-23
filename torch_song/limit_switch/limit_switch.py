class LimitSwitch:

    def __init__(self, mcp, io):
        self.mcp = mcp
        self.io = io

    def get_state(self):
        return not self.mcp.get_state()[self.io]
