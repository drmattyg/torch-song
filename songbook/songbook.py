import yaml
from ..MCP.mcp import MCPInput
import RPi.GPIO as GPIO

class Songbook:

	def __init__(self, filename="conf/default.yml"):
		self.conf = yaml.load(open(filename, "r").read())

	def init_gpio(self):
		GPIO.setmode(GPIO.BCM)
		for edge in self.conf["edge"]:
			for subsys in self.conf["subsystems"]["output"]:
				if "gpio" in e[subsys]:
					GPIO.setup(e[subsys], GPIO.OUT)
			for subsys in self.conf["subsystems"]["input"]:
				if "gpio" in e[subsys]:
					GPIO.setup(e[subsys], GPIO.IN)

	def init_mcp(self, mcp_config):
		return MCPInput(mcp_config["addr"], mcp_config["range"])
