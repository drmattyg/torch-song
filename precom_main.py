#!/usr/bin/env python

from torch_song.torch_song import TorchSong
from torch_song.songbook import Songbook
from torch_song.songbook import SongbookRunner


def main():
    ts = TorchSong(num_edges=3)
    sb = Songbook.from_string("songbooks/one_edge_test.yml", ts)
    runner = SongbookRunner(sb, ts)
    runner.run()
    for e in ts.edges.values():
        e.kill()


if __name__ == '__main__':
    try:
        main()
    finally:
        import default_io
