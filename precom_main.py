#!/usr/bin/env python

from torch_song import TorchSong


def main():
    ts = TorchSong(num_edges=1)
    ts.calibrate()


if __name__ == '__main__':
    main()
