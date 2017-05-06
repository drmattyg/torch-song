import yaml
import time
from torch_song.songbook.measure import Measure

IGNITER_OFFSET = 3000


class Songbook:
    def __init__(self, filename, calibration):
        self.songbook = yaml.load(open(filename, "r").read())
        self.timepoints = {}
        self.calibration = calibration
        self.sorted_timepoints = None
        self.generate_timing_map()

    def generate_timing_map(self):
        for measure in self.songbook['songbook']:
            start_time = measure['start_at']
            if start_time not in self.timepoints:
                self.timepoints[start_time] = []
            for e in measure['edges']:
                id = e['edge']
                if 'flame' in e:
                    flame_state = int(e['flame'])
                    tx_valve = Measure.Transition(Measure.VALVE, id, flame_state)
                    self.timepoints[start_time].append(tx_valve)
                    if flame_state == 1:
                        ignitor_start_time = start_time - IGNITER_OFFSET
                        if not ignitor_start_time in self.timepoints:
                            self.timepoints[ignitor_start_time] = []
                        self.timepoints[ignitor_start_time].append(
                            Measure.Transition(Measure.IGNITER, id, 1))
                        self.timepoints[start_time].append(
                            Measure.Transition(Measure.IGNITER, id, 0))
                if 'dir' in e:
                    edge_calibration = self.calibration.get_calibration(int(id))
                    distance = e['distance'] if 'distance' in e else 1
                    t = float(measure['time'])
                    direction = int(e['dir'])
                    speed = edge_calibration.get_speed(t, distance=distance)
                    tx_motor = Measure.Transition(Measure.MOTOR, id,
                                                  Measure.MotorState(direction, speed))
                    self.timepoints[start_time].append(tx_motor)
        self.sorted_timepoints = sorted(self.timepoints.keys())


class SongbookRunner:
    def __init__(self, songbook, torch_song, handlers=None):
        self.songbook = songbook
        self.torch_song = torch_song
        if handlers is None:
            handlers = {t: (lambda x: print(x)) for t in [Measure.IGNITER, Measure.MOTOR,
                                                          Measure.VALVE]}  # stub transition behavior; should replace this with appropriate callbacks
        self.handlers = handlers

    def run(self):
        t0 = time.time() * 1000
        for ts in self.songbook.sorted_timepoints:
            now = time.time()
            if now - t0 < ts:
                time.sleep(ts - (now - t0))
            for tx in enumerate(self.songbook.timepoints[ts]):
                self.execute_transiton(tx)

    def execute_measure(self, tx):
        self.handlers[tx.type](tx)
