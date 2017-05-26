import time


class TSEdgeCalibration:
    PLACEHOLDER_CALIBRATION = 4000.0
    LIMIT_SWITCH_TEST_TIME = 0.2

    def __init__(self, edge, calibration_travel_time=None):
        """

        :param id: Edge to calibrate
        :param calibration_travel_time: End to end travel time in ms.
        """
        self.edge = edge
        if calibration_travel_time is not None:
            self.calibration_travel_time = float(calibration_travel_time)
        else:
            self.calibration_travel_time = float(self.run_calibration())

    def get_speed(self, time, distance=1):
        """

        :param time: desired travel time, in milliseconds
        :param distance: optional: travel distance from 0 to 1.  Default = 1
        :return: Speed value for PWM from 0 to 255
        """
        # returns value from 0 to 255
        return int(255.0 * distance * self.calibration_travel_time / time)

    def run_calibration(self):
        e = self.edge
        # make sure it's not pinned before we start
        if any(e.get_limit_switch_state()):
            e.set_motor_state(1, 150)
            time.sleep(TSEdgeCalibration.LIMIT_SWITCH_TEST_TIME)
            e.set_motor_state(1, 0)
            if any(e.get_limit_switch_state()):
                e.set_motor_state(-1, 150)
                time.sleep(TSEdgeCalibration.LIMIT_SWITCH_TEST_TIME)
                e.set_motor_state(1, 0)
            if any(e.get_limit_switch_state()):
                # try a bit faster
                e.set_motor_state(1, 200)
                time.sleep(TSEdgeCalibration.LIMIT_SWITCH_TEST_TIME)
                e.set_motor_state(1, 0)
            if any(e.get_limit_switch_state()):
                e.set_motor_state(-1, 200)
                time.sleep(TSEdgeCalibration.LIMIT_SWITCH_TEST_TIME)
                e.set_motor_state(1, 0)
            if any(e.get_limit_switch_state()):
                raise Exception("Shit, my limit switch is stuck or some shit")
        # todo: actual calibration
        return TSEdgeCalibration.PLACEHOLDER_CALIBRATION


class TSCalibration:
    def __init__(self, config):
        self.config = config
        self.edge_map = {}
        self.run_calibration()

    def run_calibration(self):
        # todo implement this; currently this is a placeholder
        self.edge_map = {e: TSEdgeCalibration(e) for e in range(9)}

    def get_calibration(self, id):
        return self.edge_map[id]
