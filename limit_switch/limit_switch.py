import RPi.GPIO as GPIO

class LimitSwitch:



	def __init__(self, ch):
		GPIO.setup(ch, GPIO.IN)
		self.channel = ch

	def get_state_raw(self):
		return GPIO.input(self.channel)

	