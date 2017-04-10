import yaml

from calibration import TSCalibration
from songbook import Songbook


def test_songbook_parser():
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)
    example_songbook = "songbook/example.yml"
    songbook = Songbook(example_songbook, TSCalibration(config))
    print(songbook.timepoints)
