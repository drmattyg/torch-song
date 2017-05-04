import time
import click

from torch_song.calibration import TSCalibration
from torch_song.simulator import SimTorchSong
from torch_song.songbook import Songbook
import curses


def main(scr):
    scr.nodelay(1)
    ts = SimTorchSong(scr)
    for ix, edge in enumerate(ts.edges):
        edge.motor_speed = 80 - ix * 2
        edge.position = ix / 20
        edge.valve = True
        edge.igniter = True
        edge.start()
    try:
        while True:
            ts.render()
            time.sleep(0.1)
            for edge in ts.edges:
                if edge.limit_switches[0] or edge.limit_switches[1]:
                    edge.motor_direction *= -1
                    edge.valve = 1 - edge.valve
            s = scr.getstr()
            if s == "q":
                break
    except KeyboardInterrupt:
        ts.kill()


@click.argument('songbook')
def ts_cli(songbook):
    """

    :param songbook: A path to a songbook yml file to load
    :return:
    """

    # stub calibration
    calibration = TSCalibration(None)
    sb = Songbook(songbook, calibration)


if __name__ == "__main__":
    curses.wrapper(main)
