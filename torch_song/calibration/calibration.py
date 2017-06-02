import time
import numpy

def try_decorator(func):
    timeout = 10
    def wrap(*args, **kwargs):
        then = time.time()
        while ((time.time() - then) < timeout):
            if (func(*args, **kwargs)):
                return True
        return False
    return wrap

class EdgeCalibration:
    MIN_SPEED = 50
    CAL_SPEED_STEP = 5

    def __init__(self, edge):
        self.edge = edge
        self.map_entries = []
        self.fwd_speed_map = []
        self.rev_speed_map = []
        self.polarity = True

    def get_speed(self, time, distance=1):
        return int(numpy.interp(speed, self.map_entries, self.fwd_speed_map))

    @try_decorator
    def chk_beg_limit(self):
        return self.edge.get_limit_switch_state()[0]

    @try_decorator
    def chk_end_limt(self):
        return self.edge.get_limit_switch_state()[1]

    @try_decorator
    def chk_any_limt(self):
        return any(self.edge.get_limit_switch_state())

    def calibrate_one_speed(self, speed):
        e = self.edge
        # move to start
        e.set_motor_state(-1, 75)
        if (not chk_beg_limit()):
            e.set_motor_state(0, 0)
            raise Exception('Calibration timeout')
        e.set_motor_state(0, 0)

        # go forward
        then = time.time()
        e.set_motor_state(1, speed)
        if (not chk_end_limit()):
            e.set_motor_state(0, 0)
            raise Exception('Calibration timeout')
        e.set_motor_state(0, 0)
        fwd_time = time.time() - then

        # go backward
        then = time.time()
        e.set_motor_state(-1, speed)
        if (not chk_beg_limit()):
            e.set_motor_state(0, 0)
            raise Exception('Calibration timeout')
        e.set_motor_state(0, 0)
        rev_time = time.time() - then

        return [rev_time, fwd_time]

    def calibrate(self):
        j = 0
        for i in range(MIN_SPEED, 100+1, CAL_SPEED_STEP):
            res = calibrate_one_speed(i)
            self.map_entries[j] = i
            self.fwd_speed_map[j] = res[0]
            self.rev_speed_map[j] = res[1]
            j = j + 1

class Calibration:
    def __init__(self, config):
        self.config = config
        self.edge_map = {}
        self.run_calibration()

    def run_calibration(self):
        # todo implement this; currently this is a placeholder
        self.edge_map = {e: TSEdgeCalibration(e) for e in range(9)}

    def get_calibration(self, id):
        return self.edge_map[id]
