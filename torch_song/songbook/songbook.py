import yaml
import time
from torch_song.songbook.measure import Measure

MTransition = Measure.Transition
IGNITER_OFFSET = 3000
IGNITER_DELAY = 1000


class Songbook:
    def __init__(self, filename, calibration):
        self.songbook = yaml.load(open(filename, "r").read())
        self.timepoints = {}
        self.calibration = calibration
        self.sorted_timepoints = None
        self.generate_timing_map()

    # todo: 1) Add stop events.
    # todo: 2) Normalize simulator API with hardware API for motor_driver, valve, igniter, etc

    def add_transition(self, ts, tx):
        if ts not in self.timepoints:
            self.timepoints[ts] = []
        self.timepoints[ts].append(tx)

    def generate_timing_map(self):
        for measure in self.songbook['songbook']:
            start_time = measure['start_at']
            for e in measure['edges']:
                id = e['edge']
                if 'flame' in e:
                    flame_state = int(e['flame'])
                    tx_valve = MTransition(Measure.VALVE, id, flame_state)
                    self.add_transition(tx_valve, start_time)
                    if flame_state == 1:
                        igniter_start_time = start_time - IGNITER_OFFSET
                        self.add_transition(MTransition(Measure.IGNITER, id, 1), igniter_start_time)
                        self.add_transition(MTransition(Measure.IGNITER, id, 0),
                                            start_time + IGNITER_DELAY)
                    if 'dir' in e:
                        edge_calibration = self.calibration.get_calibration(int(id))
                        distance = e['distance'] if 'distance' in e else 1
                        t = float(measure['time'])
                        direction = int(e['dir'])
                        speed = edge_calibration.get_speed(t, distance=distance)
                        tx_motor = MTransition(Measure.MOTOR, id,
                                               Measure.MotorState(direction, speed))
                        self.add_transition(start_time, tx_motor)
                        tx_motor_off = MTransition(Measure.MOTOR, id,
                                                   Measure.MotorState(direction, 0))
                        self.add_transition(start_time + time, tx_motor_off)
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
            for tx in self.songbook.timepoints[ts]:
                self.execute_measure(tx)

    def execute_measure(self, tx):
        edge = self.torch_song.edges[tx.id]
        if tx.type == Measure.VALVE:
            edge.set_valve_state(tx.value)
        elif tx.type == Measure.IGNITER:
            edge.set_igniter_state(tx.value)
        elif tx.type == Measure.MOTOR:
            edge.set_motor_state(tx.value.direction, tx.value.speed)
