import Adafruit_GPIO.MCP230xx as MCP
import Adafruit_GPIO as GPIO
import time
mcp = MCP.MCP23017(busnum = 1, address = 0x20)
mcp.setup(0, GPIO.OUT)
while True:
	mcp.output(0, 1)
	time.sleep(0.5)
	mcp.output(0, 0)
	time.sleep(0.5)