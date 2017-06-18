#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
   Implements Vnet on Serial transport via Serial interface.
   This module is not multi thread safe.
"""
import time
import logging
try:
    import serial
except Exception:
    print("Warning: Serial library did not load.")

logger = logging.getLogger('IsoInterface')

DEFAULT_COM_PORT = '/dev/ttyUSB0'
COMM_TMO_SEC = 10

class IsoInterface:

    def __init__(self, comPort = DEFAULT_COM_PORT):
        self.comPort = comPort 
        self.rxbuf = 1024
        self.rxtimeout = COMM_TMO_SEC
        self.__SerialHandle = None
        self.__LastTxTime =  None
        return

    def OpenSerial(self):
        """ Opens the Serial on port X  """
        retVal = False
        try:
            if self.__SerialHandle:
                retVal = True
            else:
                self.__SerialHandle = serial.Serial(port = self.comPort,
                                                          baudrate = 9600,
                                                          timeout  = COMM_TMO_SEC
                                                          )
                logger.info('Serial port %s opened and initialized',
                             str(self.comPort))
            retVal = True
        except Exception as e:
            logger.info('Could not open com port: %s', str(e))
        return retVal

    def CloseSerial(self):
        """ Close the Serial """

        try:
            logger.debug('Closing Serial')
            #If you uncomment this there may be issues recovering when USB cable is disconnected
            #if VnetSerial.__SerialHandle:
            #   VnetSerial.__SerialHandle.halt()
            if self.__SerialHandle:
                self.__SerialHandle.close()

        except Exception as e:
            logger.info('Could not close serial port: %s', str(e))

        logger.info('Closed Serial')
        self.__SerialHandle = None

    def ReceiveMessage(self,timeoutSec=COMM_TMO_SEC):
        """ Receive a message from the Serial port """
        try:
            retVal = None
            rxbuf = self.rxbuf
            self.__SerialHandle.timeout = timeoutSec
            retVal = self.__SerialHandle.read(size = rxbuf)
        except Exception as e:
            logger.info('Exception %s', str(e))
        return retVal
