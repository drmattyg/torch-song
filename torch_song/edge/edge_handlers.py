import logging
import json

from logging.handlers import DatagramHandler

# Print a color-coded log message to console
class EdgeStreamHandler(logging.StreamHandler):
    DEFAULT = '\x1b[0m'
    RED     = '\x1b[31m'
    GREEN   = '\x1b[32m'
    YELLOW  = '\x1b[33m'
    BLUE    = '\x1b[33m'
    MAGENTA = '\x1b[35m'
    CYAN    = '\x1b[36m'
    WHITE   = '\x1b[37m'
    BOLD    = '\x1b[1m'

    colormap = {
        0: DEFAULT,
        1: RED,
        2: CYAN,
        3: MAGENTA,
        4: GREEN,
        5: YELLOW,
        6: BLUE,
        7: MAGENTA,
        8: WHITE,
        9: BOLD + RED

    }

    def __init__(self, stream=None):
        logging.StreamHandler.__init__(self, stream)

    def format(self, record):
        color_id = record.__dict__.get('edge_id', 0)
        if (record.levelname == 'ERROR'):
            color_id = 9
        text = logging.StreamHandler.format(self, record)
        color = self.colormap[color_id]
        return color + text + self.DEFAULT

# Send a JSON logm message to a server
class SocketEdgeHandler(logging.handlers.DatagramHandler):
    def __init__(self, host, remote_port):
        logging.handlers.DatagramHandler.__init__(self, host, remote_port)

    def emit(self, record):
        obj = {
            'message': record.getMessage(),
            'time': record.created,
            'filename': record.filename,
            'levelname': record.levelname,
            'funcname': record.funcName,
            'levelno': record.levelno,
            'lineno': record.lineno,
            'pathname': record.pathname,
            'edge_id': record.__dict__.get('edge_id', None)
        }
        self.send(json.dumps(obj).encode())

