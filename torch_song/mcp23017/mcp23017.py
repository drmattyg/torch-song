import Adafruit_GPIO.MCP230xx as MCP
import Adafruit_GPIO as GPIO

class MCPInput:
    def __init__(self, i2c_address, max_bit):
        self.i2c_address = i2c_address
        self.bit_range = range(0, max_bit) # the bits we're interested in
        self._mcp = MCP.MCP23017(address = i2c_address)
        if self._mcp is None:
            raise Exception("Unable to instantiate MCP")
        for b in self.bit_range:
            self._mcp.setup(b, GPIO.IN)
            self._mcp.pullup(b, True)
        self.update()

    def update(self):
        self.state = self._mcp.input_pins(self.bit_range)
        return self.state

    def all_true(self):
        return not (False in self.state)

    def all_false(self):
        return not (True in self.state)


