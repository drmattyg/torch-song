import RPi.GPIO as GPIO
import threading
from datetime import datetime
import time

class LimitSwitch:

	GO = 1
	STOP = 0

	def __init__(self, ch):
		GPIO.setup(ch, GPIO.IN)
		self.channel = ch
		self.current_state = self.get_state_raw()
		self.change_callback = None
		self.__run_thread = True
		self._thread = None

	def __del__(self):
		self.kill()

	def kill(self):
		self.__run_thread = False

	def get_state_raw(self):
		return GPIO.input(self.channel)

	def get_state(self):
		return self.current_state

	def set_change_callback(self, cb):
		self.change_callback = cb
		self._thread = threading.Thread(target = self._monitor_debouce)
		self._thread.start()

	def thread_is_alive(self):
		if not self._thread:
			return False
		return self._thread.isAlive()

	@staticmethod
	def millis():
		return int(round(datetime.now().microsecond*1000))

	def _monitor_debouce(self, debounce_count=10):
		current_millis = 0
		counter = 0
		while(self.__run_thread):
			reading = self.get_state_raw()
			if reading == self.current_state and counter > 0:
				counter = counter - 1
			if reading != self.current_state:
				counter = counter + 1
			if counter > debounce_count:
				counter = 0
				self.current_state = reading
				if self.change_callback is not None:
					self.change_callback(self.current_state)




	