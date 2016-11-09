import RPi.GPIO as GPIO
from limit_switch import LimitSwitch
class MotorDriver:
	FORWARD = 0
	REVERSE = 1

	def __init__(self, drive_channel, direction_channel):
		self.drive_channel = drive_channel
		self.direction_channel = direction_channel
		self.direction = None
		GPIO.setup(drive_channel, GPIO.OUT)
		GPIO.setup(direction_channel, GPIO.OUT)
		self.pwm = GPIO.PWM(drive_channel, 10000) # max is 20kHz according to docs
		GPIO.setup(direction_channel, GPIO.OUT)
		self.set_direction(MotorDriver.FORWARD)
		self.speed = 0

	def set_direction(self, dir):
		if dir not in [MotorDriver.FORWARD, MotorDriver.REVERSE]:
			raise ValueError("Incorrect value for set_direction")
		self.direction = dir
		GPIO.output(self.direction_channel, dir)


	def _drive_raw(self, speed, direction):
		self.set_direction(direction)
		if not (0.0 <= speed <= 100.0):
			raise ValueError("Speed must be between 0 and 100")
		self.pwm.start(speed)

	def start(self):
		self.pwm.start(self.speed)

	def stop(self):
		self.pwm.stop()

	def reverse(self):
		self.set_direction(1 - self.direction)


	def set_speed(self, speed):
		if not (0.0 <= speed <= 100.0):
			raise ValueError("Speed must be between 0 and 100")
		self.speed = speed
		self.pwm.ChangeDutyCycle(speed)

	def drive(self, speed, direction, limit_switch_1, limit_switch_2):

		def _stop_callback(state):
			if state == LimitSwitch.STOP:
				self.stop()
		
		for ls in [limit_switch_1, limit_switch_2]:
			ls.set_change_callback(_stop_callback)

		self.__drive_raw(speed, direction)




