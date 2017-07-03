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

        if command['id'] in self.server.torchsong.edges:
            if 'override' in command:
                self.server.torchsong.edges[command['id']].set_override(command['override'])
            if 'valve' in command:
                self.server.torchsong.edges[command['id']].set_valve_state_external(command['valve'])
            if 'igniter' in command:
                self.server.torchsong.edges[command['id']].set_igniter_state_external(command['igniter'])
            if 'dir' in command:
                self.server.torchsong.edges[command['id']].set_motor_state_external(
                        command['dir'], command['speed'])
        if 'stop' in command:
            logging.info('Stopping current song')
            self.server.songbook_manager.request_stop()
        if 'play' in command:
            logging.info('Restarting')
            self.server.songbook_manager.request_play()
        if 'next' in command:
            logging.info('Next song')
            self.server.songbook_manager.request_next()
        if 'prev' in command:
            logging.info('Prev song')
            self.server.songbook_manager.request_prev()
        if 'calibrate' in command:
            logging.info('Calibrating')
            self.server.songbook_manager.request_stop()
            self.server.torchsong.calibrate()

class TorchControlServer(UDPServer):
    def __init__(self, local_port, remote_port, torchsong, songbook_manager):
        UDPServer.__init__(self, ('localhost', local_port), TorchRequestHandler)

        self.torchsong = torchsong
        self.songbook_manager = songbook_manager

        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_socket.connect(('localhost', remote_port))

        self.status_updater = Thread(target = self._status_updater_loop)
        self.status_updater.setDaemon(True)
        self.status_updater.start()

    def send_data(self):
        obj = {}
        for k,v in self.torchsong.edges.items():
            obj[k] = {}
            obj[k]['position'] = v.get_position()
            obj[k]['igniter'] = v.get_igniter_state()
            obj[k]['valve'] = v.get_valve_state()
            obj[k]['rev_limit'] = v.get_reverse_limit_switch_state()
            obj[k]['fwd_limit'] = v.get_forward_limit_switch_state()
        t = self.songbook_manager.get_song_times()
        obj['current_song'] = self.songbook_manager.current_song()
        obj['next_song'] = self.songbook_manager.next_song()
        obj['current_song_time'] = t[0]
        obj['end_song_time'] = t[1]
        try:
            self.send_socket.send(json.dumps(obj).encode())
        except ConnectionRefusedError:
            pass

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
