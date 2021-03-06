import time
import numpy
import logging

from torch_song.common import try_decorator

class EdgeCalibration:
    def __init__(self, edge, min_speed=80, cal_speed_step=20):
        self.edge = edge

        self.duty_cycle_map = [80]
        self.fwd_time_map = [6]
        self.rev_time_map = [6]

        self.duty_cycle_map_reversed = [80]
        self.fwd_time_map_reversed = [6]
        self.rev_time_map_reversed = [6]

        self.polarity = False
        self.min_speed = min_speed
        self.cal_speed_step = cal_speed_step

    def __str__(self):
        return (str(self.duty_cycle_map_reversed) + '\n\r' +
                str(self.fwd_time_map_reversed) + '\n\r' +
                str(self.rev_time_map_reversed) + '\n\r' +
                'polarity:' + str(self.polarity))

    def serialize(self):
        return {
            'polarity': self.polarity,
            'duty_cycle_map': self.duty_cycle_map,
            'duty_cycle_map_reversed': self.duty_cycle_map_reversed,
            'fwd_time_map':  self.fwd_time_map,
            'rev_time_map': self.rev_time_map,
            'fwd_time_map_reversed': self.fwd_time_map_reversed,
            'rev_time_map_reversed': self.rev_time_map_reversed,
        }

    def deserialize(self, obj):
        self.polarity = obj['polarity']
        self.duty_cycle_map = obj['duty_cycle_map']
        self.duty_cycle_map_reversed = obj['duty_cycle_map_reversed']
        self.fwd_time_map = obj['fwd_time_map']
        self.rev_time_map = obj['rev_time_map']
        self.fwd_time_map_reversed = obj['fwd_time_map_reversed']
        self.rev_time_map_reversed = obj['rev_time_map_reversed']

    def get_motor_speed(self, time, direction, distance=1):
        if (direction == 1):
            return int(
                numpy.interp(time * distance / 1000,
                self.fwd_time_map_reversed, self.duty_cycle_map_reversed))
        elif (direction == -1):
            return int(
                numpy.interp(time * distance / 1000,
                self.rev_time_map_reversed, self.duty_cycle_map_reversed))
        else:
            return 0

    # Returns the calibrated time for end-to-end travel
    def get_cal_time(self, duty_cycle, direction):
        if (len(self.duty_cycle_map) == 0):
            return 1
        if (direction == 1):
            return numpy.interp(duty_cycle, self.duty_cycle_map, self.fwd_time_map)
        elif (direction == -1):
            return numpy.interp(duty_cycle, self.duty_cycle_map, self.rev_time_map)
        else:
            return 0

    @try_decorator()
    def chk_beg_limit(self):
        return self.edge.get_limit_switch_state()[1 if self.polarity else 0]

    @try_decorator()
    def chk_end_limit(self):
        return self.edge.get_limit_switch_state()[0 if self.polarity else 1]

    @try_decorator()
    def chk_any_limit(self):
        return any(self.edge.get_limit_switch_state())

    def calibrate_polarity(self):
        e = self.edge
        e.set_motor_state(-1, 75)
        time.sleep(.5)
        if (not self.chk_any_limit()):
            e.set_motor_state(0, 0)
            raise Exception('Calibration timeout')
        e.set_motor_state(0, 0)
        self.polarity = False if self.edge.get_limit_switch_state()[0] else True
        logging.info('Calibrated polarity for edge:%d is %d' % (self.edge.id, self.polarity),
                extra={'edge_id': self.edge.id}) 
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

        logging.info('Calibrated edge:%d at spd:%d is fwd:%f rev:%f' %
            (self.edge.id, speed, fwd_time, rev_time), extra={'edge_id': self.edge.id})

        return [fwd_time, rev_time]

    def calibrate(self):
        self.duty_cycle_map = []
        self.fwd_time_map = []
        self.rev_time_map = []

        self.calibrate_polarity()
        for i in range(self.min_speed, 100 + 1, self.cal_speed_step):
            res = self.calibrate_one_speed(i)
            self.duty_cycle_map.append(i)
            self.fwd_time_map.append(res[0])
            self.rev_time_map.append(res[1])

        self.duty_cycle_map_reversed = list(self.duty_cycle_map)
        self.duty_cycle_map_reversed.reverse()
        self.fwd_time_map_reversed = list(self.fwd_time_map)
        self.fwd_time_map_reversed.reverse()
        self.rev_time_map_reversed = list(self.rev_time_map)
        self.rev_time_map_reversed.reverse()

        self.edge.home()
