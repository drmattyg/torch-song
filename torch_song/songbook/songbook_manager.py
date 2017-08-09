import time
from threading import Event, Lock
import logging
import itertools
import random

from torch_song.songbook import Songbook
from torch_song.songbook import SongbookRunner
from torch_song.sound.sound import Sound
from torch_song.common import interruptable_sleep
from torch_song.icosahedron.icosahedron import Icosahedron
from os import path

class SongbookManager:
    def __init__(self, songbooks, torchsong, mode='manual'):
        self.songbooks = songbooks
        self.torchsong = torchsong
        self.sound_module = Sound()

        self.songbook_iterator = itertools.cycle(self.songbooks)

        self.kill_signal = Event()
        self.is_stopped = Event()
        self.next_song_request = Event()
        self.next_song_number = -1
        self.lock = Lock()

        self.set_mode(mode)
        if (self.mode == 'test'):
            self.next_up = 'songbooks/nine_edge_test.yml'
        else:
            self.next_up = next(self.songbook_iterator)

        def icosahedron_callback(self, song_number):
            self.next_song_request.set()
            self.lock.acquire()
            self.next_song_number = song_number
            self.lock.release()
            logging.info('Icosahedron request for song ' + int(song_number))

        self.icosahedron = Icosahedron(icosahedron_callback)

        self.is_stopped.set()

    def set_mode(self, mode):
        if (mode == 'test' or mode == 'playa'):
            self.mode = mode
        else:
            raise Exception('avail modes are "playa" or "test". unknown song manager mode:', mode)

    def request_song(self):
        pass

    def request_stop(self, block):
        self.is_stopped.set()
        if hasattr(self, 'runner'):
            self.runner.request_stop(block)
        self.torchsong.turn_off()

    def request_play(self):
        self.is_stopped.clear()

    def request_next(self):
        if hasattr(self, 'runner'):
            self.runner.request_stop()
        self.next_song_request.set()

    def current_song(self):
        if hasattr(self, 'runner'):
            return self.runner.name()
        else:
            return 'None'

    def next_song(self):
        return path.basename(self.next_up)

    def get_song_times(self):
        if hasattr(self, 'runner'):
            return self.runner.get_song_times()
        else:
            return [0, 0]

    def kill(self):
        if (not self.kill_signal.is_set()):
            logging.info('Stopping songbook manager')
            self.kill_signal.set()
            if hasattr(self, 'runner'):
                self.runner.request_stop()

    def __del__(self):
        self.kill()

    def run(self):
        while (not self.kill_signal.is_set()):
            if (self.is_stopped.is_set()):
                time.sleep(1)
            elif (self.mode == 'test'):
                self.torchsong.home()
                self.next_song_request.clear()
                sb = Songbook(self.next_up, self.torchsong)
                self.runner = SongbookRunner(sb, self.torchsong, self.sound_module)
                self.next_up = 'songbooks/nine_edge_test.yml'
                self.runner.run()
                self.torchsong.turn_off()
            elif (self.mode == 'playa'):
                self.torchsong.home()
                self.torchsong.go_middle()
                interruptable_sleep(5, self.next_song_request)
                while (not self.next_song_request.is_set()):
                    if (self.is_stopped.is_set() or self.kill_signal.is_set()):
                        break
                    self.torchsong.puff()
                    interruptable_sleep(9, self.next_song_request)
                self.next_song_request.clear()
                if (self.is_stopped.is_set() or self.kill_signal.is_set()):
                    pass
                else:
                    self.torchsong.home()
                    if self.next_song_number is not -1:
                        self.lock.acquire()
                        sn = self.next_song_number % len(self.songbooks)
                        self.next_up = self.songbooks[sn]
                        self.next_song_number = -1
                        self.lock.release()
                    else:
                        self.next_up = random.choice(self.songbooks)
                    sb = Songbook(self.next_up, self.torchsong)
                    self.runner = SongbookRunner(sb, self.torchsong, self.sound_module)
                    self.runner.run()
                    self.torchsong.turn_off()

