import logging
import json
from torch_song.edge import AbstractEdge
from socketserver import UDPServer, BaseRequestHandler

# Handle requests
class EdgeRequestHandler(BaseRequestHandler):
    def handle(self):
        command = {}
        try:
            req = self.request[0].decode('utf-8')
            command = json.loads(req)
        except:
            logging.error('Failed to parse JSON command')

        if 'override' in command:
            self.server.edges[command['id']].set_override(command['override'])
        if 'valve' in command:
            self.server.edges[command['id']].set_valve_state_external(command['valve'])
        if 'igniter' in command:
            self.server.edges[command['id']].set_igniter_state_external(command['igniter'])
        if 'dir' in command:
            self.server.edges[command['id']].set_motor_state_external(
                    command['dir'], command['speed'])

class EdgeControlServer(UDPServer):
    def __init__(self, port, edges):
        UDPServer.__init__(self, ('localhost', port), EdgeRequestHandler)
        self.edges = edges
    def kill(self):
        self.shutdown()
        self.server_close()
    def __del__(self):
        self.kill()

class EdgeControlMux(AbstractEdge):
    def __init__(self, edge):
        super().__init__(edge.id)
        self.override = False
        self.edge = edge

    def set_override(self, override):
        msg = "Enabled override" if override else "Disabled override"
        logging.info(msg, extra={'edge_id': self.edge.id})
        self.override = override

    def set_motor_state(self, direction, speed):
        if (not self.override):
            self.edge.set_motor_state(direction, speed)

    def set_motor_state_external(self, direction, speed):
        if (self.override):
            self.edge.set_motor_state(direction, speed)

    def set_valve_state(self, v):
        if (not self.override):
            self.edge.set_valve_state(v)

    def set_valve_state_external(self, v):
        if (self.override):
            self.edge.set_valve_state(v)

    def set_igniter_state(self, g):
        if (not self.override):
            self.edge.set_igniter_state(g)

    def set_igniter_state_external(self, g):
        if (self.override):
            self.edge.set_igniter_state(g)

    def get_limit_switch_state(self):
        return self.edge.get_limit_switch_state()

    def calibrate(self):
        if (not self.override):
            self.edge.calibrate()

    def calibrate_external(self):
        if (self.override):
            self.edge.calibrate()

    def get_position(self):
        return self.edge.position

    def get_calibration(self):
        return self.edge.calibration

    def kill(self):
        self.edge.kill()

    def __del__(self):
        self.kill()
