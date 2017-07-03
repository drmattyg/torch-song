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
from torch_song.songbook.songbook_manager import SongbookManager
from torch_song.server.control_udp_server import TorchControlServer
from torch_song.isocahedron import IsoInterface

songbooks = [
    #'songbooks/three_edge_chaser.yml',
    #'songbooks/points_of_light.yml'
    'songbooks/nine_edge_test.yml'
]

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hsnv", ["help", "sim", "nocal", "verbose"])
    except getopt.GetoptError:
        print('Unrecognized option')
        sys.exit(2)

    sim = False
    skipCal = False
    verbose = False
    for opt, arg in opts:
        if opt in ('-s', '--sim'):
            sim = True
        if opt in ('-n', '--nocal'):
            skipCal = True
        if opt in ('-v', '--verbose'):
            verbose = True

    # Build config
    try:
        stream = open('conf/default-mod.yml', 'r')
    except Exception:
        stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    # Create torch song
    ts = TorchSong(config=config, num_edges=config['num_edges'], sim=sim, verbose=verbose)
    sbm = SongbookManager(songbooks, ts, config['songbook_mode'])

    # Start TorchSong server
    cs_local_port = config['control_server']['local_port']
    cs_remote_port = config['control_server']['remote_port']
    cs_server = TorchControlServer(cs_local_port, cs_remote_port, ts, sbm)

    cs_server_thread = Thread(target=cs_server.serve_forever)
    cs_server_thread.daemon = True
    cs_server_thread.start()

    loops = 0
    try:
        if (not skipCal):
            ts.calibrate()
        sbm.run()
    except KeyboardInterrupt:
        logging.info('Received ctrl-c, cleaning up')
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
    finally:
        ts.kill()
        cs_server.kill()
        sys.exit(2)


if __name__ == '__main__':
    main()
