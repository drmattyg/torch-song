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

        self.edges = dict()
        edge_count = 0

        # Build edges
        if (not sim and not force_sim):
            self.io = dict()
            self.io['pca9685'] = PCA9685()
            mcps = dict()
            for m in self.config['io']['mcp23017']:
                mcp = MCPInput(m['i2c_address'], m['bits'])
                mcps[m['id']] = mcp
            self.io['mcp23017'] = mcps

            for e in self.config['edges']:
                if e['enabled'] is True:
                    id = e['id']
                    self.edges[id] = RealEdge(id, self.io, self.config, verbose)
                edge_count += 1
                if edge_count >= num_edges:
                    break

        else:
            for e in self.config['edges']:
                if e['enabled'] is True:
                    id = e['id']
                    self.edges[id] = SimEdge(id, 1000, verbose)
                edge_count += 1
                if edge_count >= num_edges:
                    break

        self.load_calibration()
        logging.info('Loaded calibration')
        # Hook up command mux
        for e in self.edges.items():
            # FIXME
            self.edges[e[0]] = EdgeControlMux(e[1], self.config['edges'][e[0] - 1])

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
        run_parallel('home', self.edges.values(), 'kill')

    def go_middle(self):
        logging.info('Going to the middle')
        run_parallel('go_middle', self.edges.values(), 'kill')

    def puff(self, t = 3):
        logging.info('Puffing')
        for e in self.edges.values():
            e.set_igniter_state(1)
        time.sleep(4)
        for e in self.edges.values():
            e.set_valve_state(1)
        time.sleep(t)
        for e in self.edges.values():
            e.set_igniter_state(0)
            e.set_valve_state(0)

    def calibrate(self):
        logging.info('Starting calibration')
        run_parallel('calibrate', self.edges.values(), 'kill')
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
