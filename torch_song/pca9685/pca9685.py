import Adafruit_PCA9685.PCA9685 as PCA

class PCA9685:
    def __init__(self, i2c_address = 0x40):
        self.i2c_address = i2c_address

        self._pca = PCA(address = i2c_address)
        if self._pca is None:
            raise Exception("Unable to instantiate PCA9685 device")
        self.set_pwm_frequency()
        self.duty = [0] * 16

    def set_pwm_frequency(self, freq = 1526):
        self._pca.set_pwm_freq(freq)

    def set_on(self, channel):
        self.set_duty(channel, 100)

    def set_off(self, channel):
        self.set_duty(channel, 0)

    def set_duty(self, channel, duty):
        self._pca.set_pwm(channel, 0, int(duty * 4095 / 100))
        self.duty[channel] = duty

    def disable(self, channel):
        self.set_off(channel)

    def disable_all(self):
        self.set_all_pwm(0, 0)

