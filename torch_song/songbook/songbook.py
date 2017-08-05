import yaml
import time
from torch_song.songbook.measure import Measure
from threading import Event
import logging
from os import path
from torch_song.common import interruptable_sleep

import pprint

MTransition = Measure.Transition
IGNITER_OFFSET = 4000
IGNITER_DELAY = 1000

class Songbook:
    def __init__(self, filename, torch_song):
        self.songbook = yaml.load(open(filename, "r").read())
        self.mp3 = None
        if 'mp3' in self.songbook:
            self.mp3 = self.songbook['mp3']
        self.timepoints = {}
        self.torch_song = torch_song
        self.sorted_timepoints = None
        self.generate_timing_map()
        self.name = path.basename(filename)

    @staticmethod
    def from_string(string, torch_song):
        _self = Songbook.__new__(Songbook);
        _self.songbook = yaml.load(string)
        _self.timepoints = {}
        _self.torch_song = torch_song
        _self.sorted_timepoints = None
        _self.generate_timing_map()
        _self.name = 'custom'
        return _self

    def __str__(self):
        return self.name

    def add_transition(self, tx, ts):
        if ts not in self.timepoints:
            self.timepoints[ts] = []
        self.timepoints[ts].append(tx)

    def generate_timing_map(self):
        for measure in self.songbook['songbook']:
            start_time = measure['start_at']
            for e in measure['edges']:
                id = e['edge']
                if not id in self.torch_song.edges:
                    continue
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
    def __init__(self, songbook, torch_song, sound_module):
        self.songbook = songbook
        self.torch_song = torch_song
        self.sound_module = sound_module
        self.pause = False
        self.stop = Event()
        self.finished = Event()

        self.start_song_time = 0
        self.current_song_time = 0
        self.end_song_time = 0

    def name(self):
        return self.__str__()

    def get_song_times(self):
        if (self.finished.is_set()):
            return [0, self.end_song_time - self.start_song_time]
        else:
            return [self.current_song_time - self.start_song_time,
                    self.end_song_time - self.start_song_time]

    def __str__(self):
        if (not self.finished.is_set()):
            return self.songbook.name
        else:
            return 'None'

    def updater(self):
        self.current_song_time = time.time() * 1000

    def run(self):
        logging.info("Starting songbook:" + self.__str__())
        self.start_song_time = time.time() * 1000
        t0 = time.time() * 1000

        # In the future we'll start the music earlier to account for negative timepoints
        # negative timepoints correspond to igniter offsets; igniters have to come on before flame
        # for now, add on the min_time

        min_time = -min(self.songbook.sorted_timepoints)
        self.end_song_time = ((self.songbook.sorted_timepoints[-1] -
                              self.songbook.sorted_timepoints[0]) + time.time() * 1000)
        if self.songbook.mp3 is not None:
            self.sound_module.play(self.songbook.mp3)
        for ts in self.songbook.sorted_timepoints:
            now = time.time() * 1000
            ts_0 = ts + min_time
            if now - t0 < ts_0:
                to_sleep = (ts_0 - (now - t0)) / 1000
                not_interrupted = interruptable_sleep(to_sleep, self.stop, self.updater)
                if (not not_interrupted):
                    break
            for tx in self.songbook.timepoints[ts]:
                self.execute_measure(tx)
        logging.info("Finished songbook:" + self.__str__())
        self.finished.set()

    def execute_measure(self, tx):
        edge = self.torch_song.edges[tx.id]
        if tx.type == Measure.VALVE:
            edge.set_valve_state(tx.value)
        elif tx.type == Measure.IGNITER:
            edge.set_igniter_state(tx.value)
        elif tx.type == Measure.MOTOR:
            edge.set_motor_state(tx.value.direction, tx.value.speed)

    # Should be called from a different thread
    def request_stop(self, block=False):
        self.stop.set()
        self.sound_module.stop()
        if (block):
            self.finished.wait(15)

