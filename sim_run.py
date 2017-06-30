#!/usr/bin/env python

import getopt
import sys
import os
import traceback
import random
import logging
import yaml

from threading import Thread

from torch_song.torch_song import TorchSong
from torch_song.songbook import Songbook
from torch_song.songbook import SongbookRunner
from torch_song.server.control_udp_server import TorchControlServer
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

    # Build config
    try:
        stream = open('conf/default-mod.yml', 'r')
    except Exception:
        stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    # Create torch song
    ts = TorchSong(config=config, num_edges=3, sim=sim)

    # Start TorchSong server
    cs_local_port = config['control_server']['local_port']
    cs_remote_port = config['control_server']['remote_port']
    cs_server = TorchControlServer(cs_local_port, cs_remote_port, ts)

    cs_server_thread = Thread(target=cs_server.serve_forever)
    cs_server_thread.daemon = True
    cs_server_thread.start()


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
        cs_server.kill()
        if (not sim):
            import default_io
        sys.exit(2)


if __name__ == '__main__':
    main()
