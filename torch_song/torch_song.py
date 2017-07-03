import time
from threading import Thread, Lock, Event
import logging
from torch_song.edge.edge_control_mux import EdgeControlMux
from torch_song.edge.edge_handlers import *
from torch_song.common import run_parallel

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

        # Setup loggersa
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        loggingPort = self.config['logging']['remote_port']

        self.socketEdgeHandler = SocketEdgeHandler('localhost', loggingPort)
        self.socketEdgeHandler.createSocket()
        self.socketEdgeHandler.setLevel(logging.INFO)

        streamHandler = EdgeStreamHandler()
        streamHandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s] %(message)s")
        streamHandler.setFormatter(formatter)

        logger.addHandler(streamHandler)
        logger.addHandler(self.socketEdgeHandler)

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

        # Hook up command mux
        for e in self.edges.items():
            self.edges[e[0]] = EdgeControlMux(e[1])

    def turn_off(self):
        for e in self.edges.values():
            e.set_valve_state(0)
            e.set_igniter_state(0)

    def kill(self):
        for e in self.edges.values():
            e.kill()

    def home(self):
        run_parallel('home', self.edges.values())

    def calibrate(self):
        run_parallel('calibrate', self.edges.values())

    def __del__(self):
        self.pleaseExit = True
        self.socketEdgeHandler.close()
