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

    def __init__(self, comPort = DEFAULT_COM_PORT):
        self.comPort = comPort
        self.rxbuf = 1024
        self.rxtimeout = COMM_TMO_SEC
        self.serial_port = None
        self.__LastTxTime =  None

        self.please_exit = Event()
        self.last_read = 0

        try:
            self.serial_port = serial.Serial(port = self.comPort, baudrate = 9600, timeout  = 0)
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
        b"abcde".decode("utf-8")
        while (not self.please_exit.is_set()):
            byte_array = b''
            b = b''
            while (b.decode('utf-8') is not '\n'):
               b = self.serial_port.read(size = 1)
               byte_array += b
            self.lock.acquire()
            self.last_read = int(byte_array.decode('utf-8'))
            self.last_read_time = time.time()
            self.lock.release()

