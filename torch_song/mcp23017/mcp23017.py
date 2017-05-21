from threading import Thread
from time import sleep, time

import Adafruit_GPIO.MCP230xx as MCP
import Adafruit_GPIO as GPIO

class MCPInput:
    def __init__(self, i2c_address, max_bit, update_rate_hz = 100):
        self.i2c_address = i2c_address
        self.bit_range = range(0, max_bit) # the bits we're interested in
        self._mcp = MCP.MCP23017(address = i2c_address)
        if self._mcp is None:
            raise Exception("Unable to instantiate MCP")
        for b in self.bit_range:
            self._mcp.setup(b, GPIO.IN)
            self._mcp.pullup(b, True)
        self.update_rate_hz = update_rate_hz

        self.runner = Thread(target = self.loop)
        self.runner.setDaemon(True)
        self.runner.start()


    def loop(self):
        self.pleaseExit = False
        while (not self.pleaseExit):
            now = time()
            self.state = self._mcp.input_pins(self.bit_range)
            tosleep = 1.0/self.update_rate_hz - (now - time())
            if (tosleep > 0):
                sleep(tosleep)

    def get_state(self):
        return self.state

    def all_true(self):
        return not (False in self.state)

    def all_false(self):
        return not (True in self.state)

    def __del__(self):
        self.pleaseExit = True
        self.runner.join(5000)

