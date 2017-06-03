#!/usr/bin/env python

import sys
from os import path
sys.path.append( path.dirname (path.dirname( path.dirname( path.abspath(__file__) ) ) ))

import curses
import threading
import time

from torch_song.simulator import SimEdge
from torch_song.calibration import EdgeCalibration

def main(scr):
    edge = SimEdge(1, 100)
    edgeCal = EdgeCalibration(edge)

    def worker():
        edgeCal.calibrate()
        print(edgeCal)
        time.sleep(1)

    worker_thread = threading.Thread(target=worker)
    worker_thread.start()

    # render loop
    def render():
        scr.nodelay(1)
        try:
            while True:
                edge.draw_str(scr, 1, 1)
                time.sleep(0.1)
                s = scr.getstr()
                if s == "q":
                    break
                if not worker_thread.is_alive():
                    break 
        except KeyboardInterrupt:
            edge.kill()

    render()
    worker_thread.join()
    edge.kill()

if __name__ == "__main__":
    curses.wrapper(main)
