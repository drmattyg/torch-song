import time
import numpy


def try_decorator(func):
    timeout = 10

    def wrap(*args, **kwargs):
        then = time.time()
        while ((time.time() - then) < timeout):
            if (func(*args, **kwargs)):
                return True
            time.sleep(0.05)
        return False

    return wrap


class EdgeCalibration:
    def __init__(self, edge, min_speed=80, cal_speed_step=20):
        self.edge = edge
        self.duty_cycle_map = []
        self.fwd_speed_map = []
        self.rev_speed_map = []
        self.polarity = False
        self.min_speed = min_speed
        self.cal_speed_step = cal_speed_step

    def __str__(self):
        return (str(self.duty_cycle_map) + '\n\r' +
                str(self.fwd_speed_map) + '\n\r' +
                str(self.rev_speed_map) + '\n\r' +
                'polarity:' + str(self.polarity))

    def get_speed(self, time, direction, distance=1):
        if (direction == 1):
            return int(
                numpy.interp(time * distance / 1000, self.fwd_speed_map, self.duty_cycle_map))
        elif (direction == -1):
            return int(
                numpy.interp(time * distance / 1000, self.rev_speed_map, self.duty_cycle_map))
        else:
            return 0

    @try_decorator
    def chk_beg_limit(self):
        return self.edge.get_limit_switch_state()[1 if self.polarity else 0]

    @try_decorator
    def chk_end_limit(self):
        return self.edge.get_limit_switch_state()[0 if self.polarity else 1]

    @try_decorator
    def chk_any_limit(self):
        return any(self.edge.get_limit_switch_state())

    def calibrate_polarity(self):
        e = self.edge
        e.set_motor_state(-1, 75)
        if (not self.chk_any_limit()):
            e.set_motor_state(0, 0)
            raise Exception('Calibration timeout')
        e.set_motor_state(0, 0)
        self.polarity = False if self.edge.get_limit_switch_state()[0] else True
        print('Calibrated polarity for edge:%d is %d' % (self.edge.id, self.polarity)) 
        return self.polarity

    def calibrate_one_speed(self, speed):
        e = self.edge
        # move to start
        e.set_motor_state(-1, 75)
        if (not self.chk_beg_limit()):
            e.set_motor_state(0, 0)
            raise Exception('Calibration timeout')
        e.set_motor_state(0, 0)

        # go forward
        then = time.time()
        e.set_motor_state(1, speed)
        if (not self.chk_end_limit()):
            e.set_motor_state(0, 0)
            raise Exception('Calibration timeout')
        e.set_motor_state(0, 0)
        fwd_time = time.time() - then

        # go backward
        then = time.time()
        e.set_motor_state(-1, speed)
        if (not self.chk_beg_limit()):
            e.set_motor_state(0, 0)
            raise Exception('Calibration timeout')
        e.set_motor_state(0, 0)
        rev_time = time.time() - then

        return [rev_time, fwd_time]

    def simple_calibrate(self, n=5):
        self.calibrate_polarity()
        cal_fwd = []
        cal_rev = []
        for i in range(n):
            cal = self.calibrate_one_speed(100)
            cal_fwd.append(cal[1])
            cal_rev.append(cal[0])
        self.fwd_speed_map = [stats.mean(cal_fwd)]
        self.rev_speed_map = [stats.mean(cal_rev)]

    def calibrate(self):
        self.calibrate_polarity()
        for i in range(self.min_speed, 100 + 1, self.cal_speed_step):
            res = self.calibrate_one_speed(i)
            self.duty_cycle_map.append(i)
            self.fwd_speed_map.append(res[0])
            self.rev_speed_map.append(res[1])
        self.duty_cycle_map.reverse()
        self.fwd_speed_map.reverse()
        self.rev_speed_map.reverse()
