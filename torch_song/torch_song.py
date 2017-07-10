import time
from threading import Thread, Lock, Event
import logging
from torch_song.edge.edge_control_mux import EdgeControlMux
from torch_song.common import run_parallel
import json

force_sim = False
try:
    from torch_song.edge.real_edge import RealEdge
    from torch_song.hardware import MCPInput
    from torch_song.hardware import PCA9685
except ImportError:
    print("Hardware imports failed, reverting to simulation")
    force_sim = True

from torch_song.simulator import SimEdge

class TorchSong:
    def __init__(self, config, num_edges=1, sim=False, verbose=False):
        # Configuration
        self.config = config
        self.cal_file = 'cal/cal.json'

        logging.info('Welcome to Torchsong')

        # Build edges
        if (not sim and not force_sim):
            self.io = dict()
            self.io['pca9685'] = PCA9685()
            mcps = dict()
            for m in self.config['io']['mcp23017']:
                mcp = MCPInput(m['i2c_address'], m['bits'])
                mcps[m['id']] = mcp
            self.io['mcp23017'] = mcps

            self.edges = {i: RealEdge(i, self.io, self.config, verbose) for i in range(1, num_edges + 1)}
        else:
            self.edges = {i: SimEdge(i, 1000, verbose) for i in range(1, num_edges + 1)}

        self.load_calibration()
        logging.info('Loaded calibration')
        # Hook up command mux
        for e in self.edges.items():
            self.edges[e[0]] = EdgeControlMux(e[1])

    def turn_off(self):
        for e in self.edges.values():
            e.set_valve_state(0)
            e.set_igniter_state(0)

    def kill(self):
        logging.info('Shutting down torchsong')
        for e in self.edges.values():
            e.kill()

    def home(self):
        logging.info('Homing')
        run_parallel('home', self.edges.values())
        logging.info('Finished Homing')

    def calibrate(self):
        logging.info('Starting calibration')
        run_parallel('calibrate', self.edges.values())
        self.save_calibration()
        logging.info('Finished and saved calibration')

    def load_calibration(self):
        with open(self.cal_file, "r") as fp:
            cal = json.load(fp)
            for e in self.edges.items():
                key = str(e[0])
                if key in cal:
                    e[1].get_calibration().deserialize(cal[key])

    def save_calibration(self):
        cal = {}
        for e in self.edges.items():
            cal[e[0]] = e[1].get_calibration().serialize()
        with open(self.cal_file, "w") as fp:
            json.dump(cal, fp)

    def __del__(self):
        self.pleaseExit = True
