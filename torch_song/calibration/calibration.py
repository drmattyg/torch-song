class TSEdgeCalibration:
    PLACEHOLDER_CALIBRATION = 4000.0

    def __init__(self, id, calibration_travel_time=None):
        """

        :param id: Int.  Edge id
        :param calibration_travel_time: End to end travel time in ms.
        """
        self.id = id
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
        # todo implement this; currently this is a placeholder
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
