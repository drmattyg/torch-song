import yaml
from torch_song.edge.real_edge import RealEdge
from torch_song.hardware import MCPInput
from torch_song.hardware import PCA9685
import time
from threading import Thread, Lock


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
        #HACK FOR PRECOM
        self.edges[1] = self.edges[4] 
        calibrators = {}

        for e in self.edges.values():
            calibrators[e.id] = Thread(target=self.worker, args=(e,))
            calibrators[e.id].start()

        for c in calibrators.values():
            c.join()

    def worker(self, edge):
        edge.calibrate()
