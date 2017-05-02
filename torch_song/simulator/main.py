import time

from torch_song.simulator import SimTorchSong
import curses


def main(scr):
    scr.nodelay(1)
    ts = SimTorchSong(scr)
    try:
        while True:
            ts.render()
            time.sleep(0.1)
            s = scr.getstr()
            if s == "q":
                break
    except KeyboardInterrupt:
        ts.kill()


if __name__ == "__main__":
    curses.wrapper(main)
