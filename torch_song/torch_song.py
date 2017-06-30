import time
from threading import Thread, Lock, Event
import traceback
import logging
from torch_song.edge.edge_control_mux import EdgeControlMux
from torch_song.edge.edge_handlers import *
from torch_song.server.control_udp_server import TorchControlServer
import os

try:
    from torch_song.edge.real_edge import RealEdge
    from torch_song.hardware import MCPInput
    from torch_song.hardware import PCA9685
except ImportError:
    print("Hardware imports failed, reverting to simulation")

from torch_song.simulator import SimEdge

class TorchSong:
    def __init__(self, config, num_edges=1, sim=False):
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

        # Hook up command mux
        for e in self.edges.items():
            self.edges[e[0]] = EdgeControlMux(e[1])

        # Start an edge command server
        cs_local_port = self.config['control_server']['local_port']
        cs_remote_port = self.config['control_server']['remote_port']
        self.server = TorchControlServer(cs_local_port, cs_remote_port, self)

        server_thread = Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        self.pos_updater = Thread(target = self._pos_updater_loop)
        self.pos_updater.setDaemon(True)
        self.pos_updater.start()

    def _pos_updater_loop(self):
        self.pleaseExit = False
        update_rate_hz = 100
        while (not self.pleaseExit):
            now = time.time()
            self.server.send_data()
            tosleep = 1.0/update_rate_hz - (time.time() - now)
            if (tosleep > 0):
                time.sleep(tosleep)


    def _worker(self, edge, event):
        try:
            edge.calibrate()
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
            event.set()

    def calibrate(self):
        calibrators = []
        events = []

        for e in self.edges.values():
            event = Event()
            calibrators.append(Thread(target=self._worker, args=(e,event,)))
            events.append(event)

        for c in calibrators:
            c.start()

        done = lambda: any(map(lambda c: not c.isAlive(), calibrators))
        is_exc = lambda: any(map(lambda e: e.is_set(), events))

        while (not done()):
            if (is_exc()):
                raise Exception('Calibration error')
            time.sleep(.1)

        if (is_exc()):
            raise Exception('Calibration error')

        for c in calibrators:
            c.join()

    def __del__(self):
        self.pleaseExit = True
        self.socketEdgeHandler.close()
        self.server.kill()
