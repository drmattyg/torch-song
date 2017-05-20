from torch_song.calibration import TSCalibration
from torch_song.simulator import SimTorchSong
from torch_song.songbook import Songbook, SongbookRunner, IGNITER_OFFSET
import nose.tools as nt
import time
import threading

SIMPLE_SONGBOOK = """
songbook:
  - start_at: 1000
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


def test_songbook_runner():
    sb = Songbook.from_string(SIMPLE_SONGBOOK, TSCalibration(None))
    ts = SimTorchSong(None)
    runner = SongbookRunner(sb, ts)
    nt.assert_false(ts.edges[0].valve)
    nt.assert_false(ts.edges[0].motor_speed)
    th = threading.Thread(target=runner.run)
    #    runner.run()
    th.start()
    print("start")
    t0 = time.time()
    time.sleep((IGNITER_OFFSET + 1000 + 100) / 1000)
    print("Time = %s" % str(time.time() - t0))
    nt.assert_true(ts.edges[0].valve)
    nt.assert_true(ts.edges[0].motor_speed > 0)
    th.join()
