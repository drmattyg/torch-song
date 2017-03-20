import RPi.GPIO as GPIO
from limit_switch import LimitSwitch
class MotorDriver:
    FORWARD = 0
    REVERSE = 1

    def __init__(self, pwm_pin, dir_pin):
        print(pwm_pin, dir_pin)
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.dir = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pwm_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(pwm_pin, 100) # max is 20kHz according to docs
        self.set_dir(MotorDriver.FORWARD)
        self.speed = 0

    def set_dir(self, dir):
        if dir not in [MotorDriver.FORWARD, MotorDriver.REVERSE]:
            raise ValueError("Incorrect value for set_dir")
        self.__dir= dir
        GPIO.output(self.dir_pin, dir)

    def _drive_raw(self, speed, dir):
        self.set_dir(dir)
        if not (0.0 <= speed <= 100.0):
            raise ValueError("Speed must be between 0 and 100")
        self.pwm.start(speed)

    def start(self):
        self.pwm.start(self.speed)

    def stop(self):
        self.pwm.stop()

    def reverse(self):
        self.set_dir(1 - self.dir)

    def set_speed(self, speed):
        if not (0.0 <= speed <= 100.0):
            raise ValueError("Speed must be between 0 and 100")
        self.speed = speed
        self.pwm.ChangeDutyCycle(speed)

    def set_freq(self, freq):
        self.pwm = GPIO.PWM(self.pwm_pin, freq) # max is 20kHz according to docs
        self.set_speed(self.speed)
        self.pwm.start(self.speed)

    def driver(self, speed, dir, limit_switch_1, limit_switch_2):

        def _stop_callback(state):
            if state == LimitSwitch.STOP:
                self.stop()
        
        for ls in [limit_switch_1, limit_switch_2]:
            ls.set_change_callback(_stop_callback)

        self.__pwm_raw(speed, dir)




