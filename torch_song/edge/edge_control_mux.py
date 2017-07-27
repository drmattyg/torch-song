import logging
from torch_song.edge import AbstractEdge

class EdgeControlMux(AbstractEdge):
    def __init__(self, edge, edge_config):
        super().__init__(edge.id)
        self.override = False
        self.edge = edge
        self.edge_config = edge_config

    def set_override(self, override):
        msg = "Enabled override" if override else "Disabled override"
        logging.info(msg, extra={'edge_id': self.edge.id})
        self.override = override

    def set_motor_state(self, direction, speed):
        if (not self.override):
            if self.edge_config['motors_enabled'] is True:
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
        return self.edge.get_position()

    def get_valve_state(self):
        return self.edge.get_valve_state()

    def get_igniter_state(self):
        return self.edge.get_igniter_state()

    def get_calibration(self):
        return self.edge.calibration

    def is_healthy(self):
        return self.edge.is_healthy()

    def kill(self):
        self.edge.kill()

    def __del__(self):
        self.kill()
