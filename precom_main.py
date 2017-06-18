#!/usr/bin/env python

import getopt
import sys
import traceback
import random

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
    iso = IsoInterface()
    try:
        ts.calibrate()
        iso.OpenSerial()
        loops = 5
        # while (loops > 0):
        while True:
            while (not len(iso.ReceiveMessage(1).decode('utf-8'))):
                pass
            while (not len(iso.ReceiveMessage(1).decode('utf-8'))):
                pass
            sb = Songbook.from_string(random.choice(songbooks), ts)
            runner = SongbookRunner(sb, ts)
            runner.run()
            for e in ts.edges.values():
                e.home()
            iso.ReceiveMessage(120)
            # loops -= 1
        for e in ts.edges.values():
            iso.CloseSerial()
            e.kill()
    except KeyboardInterrupt:
        print('Received ctrl-c, cleaning up')
    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        for e in ts.edges.values():
            iso.CloseSerial()
            e.kill()
        if (not sim):
            import default_io
        sys.exit(2)


if __name__ == '__main__':
    main()
