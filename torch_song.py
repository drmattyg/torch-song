#!/usr/bin/env python

NUM_EDGES = 9

class TorchSong:
    def __init__(self, EdgeClass):
        self.edges = {i: EdgeClass(i) for i in range(NUM_EDGES)}
