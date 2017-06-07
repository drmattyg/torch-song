#!/usr/bin/env python

from torch_song import TorchSong
from torch_song.songbook import Songbook
from torch_song.songbook import SongbookRunner


def main():
    ts = TorchSong(num_edges=1)
    sb = Songbook.from_string("songbooks/one_edge_test.yml", ts.calibration)
    runner = SongbookRunner(sb, ts)

    ts.calibrate()


if __name__ == '__main__':
    try:
        main()
    finally:
        import default_io
