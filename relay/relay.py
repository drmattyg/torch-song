import RPi.GPIO as GPIO

class Relay:
	ON = 0
	OFF = 1
	def __init__(self, gpio):
		self.gpio = gpio;
		GPIO.setup(self.gpio, GPIO.OUT)
		GPIO.output(self.gpio, Relay.OFF)
		self.__state = Relay.OFF

	def get_state(self):
		return self.__state

	def set_state(self, state):
		if state not in [Relay.ON, Relay.OFF]:
			raise Exception("Invalid value for set_state")
		self.__state = state;
		GPIO.output(self.gpio, self.__state)

	def invert(self):
		self.set_state(1 - self.__state)
