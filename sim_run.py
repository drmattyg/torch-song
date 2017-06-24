#!/usr/bin/env python

import getopt
import sys
import os
import traceback
import random
import logging

from torch_song.torch_song import TorchSong
from torch_song.songbook import Songbook
from torch_song.songbook import SongbookRunner
from torch_song.isocahedron import IsoInterface

songbooks = [
    'songbooks/three_edge_chaser.yml',
    'songbooks/points_of_light.yml'
]

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs", ["help", "sim"])
    except getopt.GetoptError:
        sys.exit(2)

    sim = False
    for opt, arg in opts:
        if opt in ('-s', '--sim'):
            sim = True

    ts = TorchSong(num_edges=4, sim=sim)
    loops = 0
    try:
        ts.calibrate()
        while True:
            sb = Songbook.from_string(random.choice(songbooks), ts)
            runner = SongbookRunner(sb, ts)
            runner.run()
            for e in ts.edges.values():
                e.home()
            loops += 1
        for e in ts.edges.values():
            e.kill()
    except KeyboardInterrupt:
        logging.info('Received ctrl-c, cleaning up')
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
    finally:
        for e in ts.edges.values():
            e.kill()
        if (not sim):
            import default_io
        sys.exit(2)


if __name__ == '__main__':
    main()
