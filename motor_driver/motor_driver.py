import RPi.GPIO as GPIO
from limit_switch import LimitSwitch
class MotorDriver:
	def FORWARD = 0
	def REVERSE = 1

	def __init__(self, drive_channel, direction_channel):
		self.drive_channel = drive_channel
		self.drive_channel = direction_channel
		self.pwm = GPIO.PWM(drive_channel, 10000) # max is 20kHz according to docs
		GPIO.setup(direction_channel, GPIO.OUT)
		self.set_direction(GPIO.FORWARD)

	def set_direction(self, dir):
		if dir not in [MotorDriver.FORWARD, MotorDriver.REVERSE]:
			raise ValueError("Incorrect value for set_direction")
		GPIO.output(self.direction_channel, dir)


	def __drive_raw(self, speed, direction):
		self.set_direction(direction)
		if not (0.0 < speed < 100.0):
			raise ValueError("Speed must be between 0 and 100")
		self.pwm.ChangeDutyCycle(speed)

	def stop(self):
		self.pwm.ChangeDutyCycle(0)

	def drive(self, speed, direction, limit_switch_1, limit_switch_2):

		def _stop_callback(state):
			if state == LimitSwitch.STOP:
				self.stop()
		
		for ls in [limit_switch_1, limit_switch_2]:
			ls.set_change_callback(_stop_callback)

		self.__drive_raw(speed, direction)




