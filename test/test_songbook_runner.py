from torch_song.calibration import TSCalibration
from torch_song.simulator import SimTorchSong
from torch_song.songbook import Songbook, SongbookRunner
import curses
import time

SIMPLE_SONGBOOK = """
songbook:
  - start_at: 0
    time: 4000
    edges:
      - edge: 0
        flame: 1
        dir: 1
  - start_at: 3000
    time: 6000
    edges:
      - edge: 1
        flame: 1
        dir: 1
      - edge: 6
        flame: 0
        dir: 0
"""


def setup_module():
    curses.initscr()
    curses.start_color()


def test_songbook_runner():
    sb = Songbook.from_string(SIMPLE_SONGBOOK, TSCalibration(None))
    ts = SimTorchSong(None)
    runner = SongbookRunner(sb, ts)
    runner.run()
    time.sleep(5)
    print(ts.edges)


def teardown_module():
    curses.endwin()
