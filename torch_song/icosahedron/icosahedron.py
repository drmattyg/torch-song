from threading import Thread, Event, Lock

import time
import logging
import copy

try:
    import serial
except Exception:
    print("Warning: Serial library did not load.")

DEFAULT_COM_PORT = '/dev/ttyUSB0'

class Icosahedron:

    def __init__(self, callback, comPort = DEFAULT_COM_PORT):
        self.comPort = comPort
        self.please_exit = Event()
        self.last_read = -1
        self.callback = callback
        self.serial_port = None

        try:
            self.serial_port = serial.Serial(port = self.comPort, baudrate = 9600, timeout  = None)
            logging.info('Serial port %s opened and initialized', str(self.comPort))

        except Exception as e:
            logging.error('Could not open com port: %s', str(e))


        self.lock = Lock()
        self.runner = Thread(target=self.loop)
        self.runner.setDaemon(True)
        self.runner.start()

    def kill(self):
        if self.serial_port:
            self.serial_port.close()
        self.please_exit.set()
        self.runner.join()

    def __del__(self):
        self.kill()

    def read_nonblocking(self):
        self.lock.acquire()
        val = copy.copy(self.last_read)
        self.lock.release()
        return self.last_read

    def loop(self):
        logging.info('here')
        if (self.serial_port is not None):
            logging.info('here2')
            while (not self.please_exit.is_set()):
                logging.info('here3')
                byte_array = b''
                b = b''
                while (b.decode('utf-8') is not '\n'):
                    logging.info('here4')
                    b = self.serial_port.read(size = 1)
                    logging.info('b', b)
                    byte_array += b
                logging.info('bytes', byte_array)
                self.lock.acquire()
                self.last_read = int(byte_array.decode('utf-8'))
                logging.info(self.last_read)
                self.callback(self.last_read)
                self.last_read_time = time.time()
                self.lock.release()

