import yaml
import time
from threading import Thread, Lock

try:
    from torch_song.edge.real_edge import RealEdge
    from torch_song.hardware import MCPInput
    from torch_song.hardware import PCA9685
except ImportError:
    print("Hardware imports failed, reverting to simulation")
    from torch_song.simulator import SimEdge

class TorchSong:
    def __init__(self, num_edges=1, sim=False):
        stream = open('conf/default.yml', 'r')
        self.config = yaml.load(stream)
        if (not sim):
            self.io = dict()
            self.io['pca9685'] = PCA9685()
            mcps = dict()
            for m in self.config['io']['mcp23017']:
                mcp = MCPInput(m['i2c_address'], m['bits'])
                mcps[m['id']] = mcp
            self.io['mcp23017'] = mcps

            self.edges = {i: RealEdge(i, self.io, self.config) for i in range(1, num_edges + 1)}
        else:
            self.edges = {i: SimEdge(i, 1000) for i in range(1, num_edges + 1)}

    def worker(self, edge):
        edge.calibrate()

    def calibrate(self):

        calibrators = {}

        for e in self.edges.values():
            calibrators[e.id] = Thread(target=self.worker, args=(e,))
            calibrators[e.id].start()

        for c in calibrators.values():
            c.join()

