import RPi.GPIO as GPIO

class MotorDriver:
    FORWARD = 0
    REVERSE = 1

    # We use the PCA9685 as an IO expander in some cases
    IO_TYPE_NAMES = ['PCA9685_IO', 'RPI_IO']

    def __init__(self, pca9685, pwm_io, dir_io, dir_io_type):
        self._pwm_io = pwm_io
        self._dir_io = dir_io
        self._dir_io_type = dir_io_type
        self._pca = pca9685

        if dir_io_type not in MotorDriver.IO_TYPE_NAMES:
            raise ValueError("Incorrect IO type for Motor Driver")

        if (dir_io_type == 'RPI_IO'):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(dir_io, GPIO.OUT)

        self.speed = -1
        self.dir = -1

        self.set_speed(0)
        self.set_dir(MotorDriver.FORWARD)

    def get_dir(self):
        return self.dir

    def set_dir(self, dir):
        if dir not in [MotorDriver.FORWARD, MotorDriver.REVERSE]:
            raise ValueError("Incorrect value for set_dir")
        if (dir != self.dir):
            if self._dir_io_type == 'PCA9685_IO':
                if dir is MotorDriver.FORWARD:
                    self._pca.set_off(self._dir_io)
                else:
                    self._pca.set_on(self._dir_io)
            elif self._dir_io_type == 'RPI_IO':
                GPIO.output(self._dir_io, dir)

            self.dir = dir

    def disable(self):
        self._pca.disable(self._pwm_io)

    def stop(self):
        self.set_speed(0)

    def reverse(self):
        self.set_dir(1 - self.dir)

    def set_speed(self, speed):
        if not (0.0 <= speed <= 100.0):
            raise ValueError("Speed must be between 0 and 100")
        if (self.speed != speed):
            self.speed = speed
            self._pca.set_duty(self._pwm_io, speed)

    def get_speed(self):
        return self.speed

    def get_dir(self):
        return self.dir

    def get_dir_str(self):
        return 'fwd' if self.dir == MotorDriver.FORWARD else 'rev'

    def __del__(self):
        self._pca.disable(self._pwm_io)
        if self._dir_io_type == 'RPI_IO':
            GPIO.setup(self._dir_io, GPIO.IN)



