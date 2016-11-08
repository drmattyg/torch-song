import Adafruit_GPIO.MCP230xx as MCP
import Adafruit_GPIO as GPIO

class MCPInput:
	def __init__(self, address, max_bit, busnum=1):
		self.address = address
		self.busnum = busnum
		self.bit_range = range(0, max_bit) # the bits we're interested in
		self._mcp = MCP.MCP23017(address, busnum=busnum)
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


