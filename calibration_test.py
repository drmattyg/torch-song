import curses
from torch_song.simulator import SimTorchSong, SimEdge, threading
import time

global finished


def main(scr):
    edge = SimEdge(0)
    edge.position = 0.5
    scr.nodelay(1)
    SimTorchSong.initialize_curses()
    global finished
    finished = False

    def runner():
        global finished
        edge.calibrate()
        print(edge.calibration)
        finished = True

    th = threading.Thread(target=runner)
    th.start()
    try:
        while not finished:
            edge.draw_str(scr, 5, 5)
            time.sleep(0.1)
            s = scr.getstr()
            if s == "q":
                break
        edge.kill()
        th.join()

    except KeyboardInterrupt:
        edge.kill()
        th.join()


if __name__ == "__main__":
    curses.wrapper(main)
