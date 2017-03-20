import RPi.GPIO as GPIO

class Relay:
    OPEN = 0
    CLOSED = 1

    def __init__(self, pin):
        self.pin = pin;
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.set_state(Relay.OPEN)

    def get_state(self):
        return self.__state

    def set_state(self, state):
        if state not in [Relay.CLOSED, Relay.OPEN]:
            raise Exception("Invalid value for set_state")
        self.__state = state;
        GPIO.output(self.pin, 1 - self.__state)

    def __del__(self):
        self.set_state(Relay.OPEN)
        GPIO.setup(self.pin, GPIO.IN)
