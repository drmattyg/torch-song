#!/usr/bin/env python

import getopt
import sys
import traceback

from torch_song.torch_song import TorchSong
from torch_song.songbook import Songbook
from torch_song.songbook import SongbookRunner

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
    try:
        ts.calibrate()
        loops = 1
        while (loops > 0):
            sb = Songbook.from_string("songbooks/three_edge_chaser.yml", ts)
            runner = SongbookRunner(sb, ts)
            runner.run()
            for e in ts.edges.values():
                e.home()
        for e in ts.edges.values():
            e.kill()
    except KeyboardInterrupt:
        print('Received ctrl-c, cleaning up')
    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        for e in ts.edges.values():
            e.kill()
        if (not sim):
            import default_io
        sys.exit(2)


if __name__ == '__main__':
    main()
