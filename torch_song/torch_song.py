import yaml
from torch_song.edge.real_edge import RealEdge
from torch_song.hardware import MCPInput
from torch_song.hardware import PCA9685
import time


class TorchSong:
    def __init__(self, num_edges=1):
        stream = open('conf/default.yml', 'r')
        self.config = yaml.load(stream)
        self.io = dict()
        self.io['pca9685'] = PCA9685()
        mcps = dict()
        for m in self.config['io']['mcp23017']:
            mcp = MCPInput(m['i2c_address'], m['bits'])
            mcps[m['id']] = mcp
        self.io['mcp23017'] = mcps

        self.edges = {i: RealEdge(i, self.io, self.config) for i in range(1, num_edges + 1)}
        time.sleep(1)

    def calibrate(self):
        for e in self.edges.values():
            e.calibration.calibrate()
            print(e.calibration)
