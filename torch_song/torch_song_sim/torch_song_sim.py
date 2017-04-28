import curses

import time
from torch_song.simulator import SimEdge


class TorchSongSim:
    def __init__(self, edge_list):
        self.edges = edge_list

    def render(self, scr):
        LEFT_PAD = 3
        TOP_PAD = 3
        ROW_PAD = 3
        scr.clear()
        for ix, edge in enumerate(self.edges):
            scr.addstr(ix * ROW_PAD + TOP_PAD, LEFT_PAD, str(edge))
        scr.noutrefresh()
        curses.doupdate()


def main(scr):
    e0 = SimEdge(0)
    e1 = SimEdge(1)
    e2 = SimEdge(2)
    e1.position = 0.5
    e1.valve = True
    e2.position = 0
    e0.position = 1
    e0.igniter = True
    sim = TorchSongSim([e0, e1, e2])
    # print(str(e0)))
    while True:
        sim.render(scr)
        time.sleep(1)


if __name__ == "__main__":
    # main(0)
    curses.wrapper(main)
