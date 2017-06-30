import yaml
import time
from torch_song.songbook.measure import Measure

MTransition = Measure.Transition
IGNITER_OFFSET = 4000
IGNITER_DELAY = 1000


class Songbook:
    def __init__(self, filename, torch_song):
        self.songbook = yaml.load(open(filename, "r").read())
        self.timepoints = {}
        self.torch_song = torch_song
        self.sorted_timepoints = None
        self.generate_timing_map()

    @staticmethod
    def from_string(yml, torch_song):
        _self = Songbook.__new__(Songbook);
        _self.songbook = yaml.load(open(yml, 'r'))
        _self.timepoints = {}
        _self.torch_song = torch_song
        _self.sorted_timepoints = None
        _self.generate_timing_map()
        return _self

    def add_transition(self, tx, ts):
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
                    edge_calibration = self.torch_song.edges[id].get_calibration()
                    distance = e['distance'] if 'distance' in e else 1
                    t = float(measure['time'])
                    direction = int(e['dir'])
                    speed = edge_calibration.get_motor_speed(t, direction, distance=distance)
                    tx_motor = MTransition(Measure.MOTOR, id,
                                           Measure.MotorState(direction, speed))
                    self.add_transition(tx_motor, start_time)
                    tx_motor_off = MTransition(Measure.MOTOR, id,
                                               Measure.MotorState(direction, 0))
                    self.add_transition(tx_motor_off, start_time + t)
        self.sorted_timepoints = sorted(self.timepoints.keys())


class SongbookRunner:
    def __init__(self, songbook, torch_song):
        self.songbook = songbook
        self.torch_song = torch_song
        self.finished = False

    def run(self):
        t0 = time.time() * 1000

        # In the future we'll start the music earlier to account for negative timepoints
        # negative timepoints correspond to igniter offsets; igniters have to come on before flame
        # for now, add on the min_time
        min_time = -min(self.songbook.sorted_timepoints)
        for ts in self.songbook.sorted_timepoints:
            now = time.time() * 1000
            ts_0 = ts + min_time
            if now - t0 < ts_0:
                time.sleep((ts_0 - (now - t0)) / 1000)
            for tx in self.songbook.timepoints[ts]:
                self.execute_measure(tx)
        self.finished = True

    def execute_measure(self, tx):
        edge = self.torch_song.edges[tx.id]
        if tx.type == Measure.VALVE:
            edge.set_valve_state(tx.value)
        elif tx.type == Measure.IGNITER:
            edge.set_igniter_state(tx.value)
        elif tx.type == Measure.MOTOR:
            edge.set_motor_state(tx.value.direction, tx.value.speed)

