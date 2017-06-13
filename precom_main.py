#!/usr/bin/env python

from torch_song.torch_song import TorchSong
from torch_song.songbook import Songbook
from torch_song.songbook import SongbookRunner

ts = TorchSong(num_edges=4)

def main():
    loops = 10
    while (loops > 0):
        sb = Songbook.from_string("songbooks/three_edge_chaser.yml", ts)
        runner = SongbookRunner(sb, ts)
        runner.run()
        for e in ts.edges.values():
            e.home()
    for e in ts.edges.values():
        e.kill()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        for e in ts.edges.values():
            e.kill()
    finally:
        for e in ts.edges.values():
            e.kill()
        import default_io
