import yaml

from songbook.measure import Measure


class Songbook:
    def __init__(self, filename, calibration):
        self.songbook = yaml.load(open(filename, "r").read())
        self.timepoints = {}
        self.calibration = calibration

    def generating_timing_map(self):
        for measure in self.songbook['songbook']:
            start_time = measure['start_at']
            if start_time not in self.timepoints:
                self.timepoints[start_time] = []
            for e in measure['edges']:
                id = e['edge']
                tx_valve = Measure.Transition(Measure.VALVE, id, e['flame'])
                edge_calibration = self.calibration.get_calibration()[int(id)]
                distance = e['distance'] if 'distance' in e else 1
                t = float(measure['time'])
                direction = int(e['dir'])
                speed = edge_calibration.get_speed(t, distance=distance)
                tx_dir = Measure.Transition(Measure.MOTOR, id, Measure.MotorState(direction, speed))
