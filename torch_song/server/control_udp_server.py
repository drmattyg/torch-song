import logging
import json
import time
import socket
from socketserver import UDPServer, BaseRequestHandler
from threading import Thread

# Handle requests
class TorchRequestHandler(BaseRequestHandler):
    def handle(self):
        command = {}
        try:
            req = self.request[0].decode('utf-8')
            command = json.loads(req)
        except:
            logging.error('Failed to parse JSON command')

        print(command)

        if 'override' in command:
            self.server.torchsong.edges[command['id']].set_override(command['override'])
        if 'valve' in command:
            self.server.torchsong.edges[command['id']].set_valve_state_external(command['valve'])
        if 'igniter' in command:
            self.server.torchsong.edges[command['id']].set_igniter_state_external(command['igniter'])
        if 'calibrate' in command:
            self.server.torchsong.edges[command['id']].calibrate_external()
        if 'dir' in command:
            self.server.torchsong.edges[command['id']].set_motor_state_external(
                    command['dir'], command['speed'])
        if 'pause' in command:
            print('pause', command)
            logging.info('pause')
            self.server.songbook_runner.pause(command['pause'])

class TorchControlServer(UDPServer):
    def __init__(self, local_port, remote_port, torchsong):
        UDPServer.__init__(self, ('localhost', local_port), TorchRequestHandler)
        print(UDPServer)
        self.torchsong = torchsong
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect(('localhost', remote_port))

        self.status_updater = Thread(target = self._status_updater_loop)
        self.status_updater.setDaemon(True)
        self.status_updater.start()

    def set_songbook_runner(self, sbr):
        self.songbook_runner = sbr

    def send_data(self):
        obj = {}
        for k,v in self.torchsong.edges.items():
            obj[k] = {}
            obj[k]['position'] = v.get_position()
            obj[k]['igniter'] = v.get_igniter_state()
            obj[k]['valve'] = v.get_valve_state()
        self.socket.send(json.dumps(obj).encode())

    def _status_updater_loop(self):
        self.pleaseExit = False
        update_rate_hz = 100
        while (not self.pleaseExit):
            now = time.time()
            self.send_data()
            tosleep = 1.0/update_rate_hz - (time.time() - now)
            if (tosleep > 0):
                time.sleep(tosleep)

    def kill(self):
        self.shutdown()
        self.server_close()
        self.pleaseExit = True
    def __del__(self):
        self.kill()
