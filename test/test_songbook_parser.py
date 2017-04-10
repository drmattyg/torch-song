import yaml

from calibration import TSCalibration
from songbook import Songbook


def test_songbook_parser():
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)
    example_songbook = "songbook/example.yml"
    calibration = TSCalibration(config)
    calibration.run_calibration()
    songbook = Songbook(example_songbook, calibration)
    print(songbook.timepoints)


if __file__ == "__main__":
    test_songbook_parser()
