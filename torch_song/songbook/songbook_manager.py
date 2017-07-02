import time
from threading import Event
import logging
import random
from torch_song.songbook import Songbook
from torch_song.songbook import SongbookRunner
from os import path

class SongbookManager:
    def __init__(self, songbooks, torchsong):
        self.songbooks = songbooks
        self.torchsong = torchsong

        self.mode = 'shuffle'
        self.next_up = random.choice(self.songbooks)
        self.last_song = self.next_up

        self.kill_signal = Event()
        self.is_stopped = Event()

    def set_mode(self, mode):
        if (mode == 'shuffle' or mode == 'inorder' or mode =='icosahedron'):
            self.mode = mode
        else:
            raise Exception('unknown song manager mode')

    def request_song(self):
        pass

    def request_stop(self):
        self.is_stopped.set()
        if hasattr(self, 'runner'):
            self.runner.request_stop()
        self.torchsong.turn_off()

    def request_play(self):
        self.is_stopped.clear()

    def request_next(self):
        if hasattr(self, 'runner'):
            self.runner.request_stop()

    def request_prev(self):
        if hasattr(self, 'runner'):
            self.next_up = self.last_up

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
        self.kill_signal.set()

    def __del__(self):
        self.kill()

    def run(self):
        while (not self.kill_signal.is_set()):
            if (self.is_stopped.is_set()):
                time.sleep(1)
            elif (self.mode == 'shuffle'):
                self.torchsong.home()
                time.sleep(5)
                self.last_up = self.next_up
                sb = Songbook(self.next_up, self.torchsong)
                self.runner = SongbookRunner(sb, self.torchsong)
                self.next_up = random.choice(self.songbooks)
                self.runner.run()
                self.torchsong.turn_off()
