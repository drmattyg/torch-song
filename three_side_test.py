import curses
import threading

import time

from torch_song.calibration import TSCalibration
from torch_song.songbook import Songbook, SongbookRunner
from torch_song.simulator import SimTorchSong

SONGBOOK_YML = """
songbook:
  - start_at: 0
    time: 4000
    edges:
      - edge: 0
        flame: 1
        dir: 1
  - start_at: 4000
    time: 4000
    edges:
      - edge: 0
        flame: 0
        dir: -1
      - edge: 1
        flame: 1
        dir: 1
  - start_at: 8000
    time: 4000
    edges:
      - edge: 1
        flame: 0
        dir: -1
      - edge: 2
        flame: 1
        dir: 1
"""


def main(scr):
    sb = Songbook.from_string(SONGBOOK_YML, TSCalibration(None))
    ts = SimTorchSong(scr, num_edges=3)
    runner = SongbookRunner(sb, ts)
    scr.nodelay(1)
    SimTorchSong.initialize_curses()
    th = threading.Thread(target=runner.run)
    th.start()
    try:
        while not runner.finished:
            ts.render()
            time.sleep(0.1)
            s = scr.getstr()
            if s == "q":
                break
        ts.kill()
        th.join()

    except KeyboardInterrupt:
        ts.kill()
        th.join()


if __name__ == "__main__":
    curses.wrapper(main)
