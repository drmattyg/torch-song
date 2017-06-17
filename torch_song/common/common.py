import time
import sys

from logging.handlers import HTTPHandler
from socket import socket

def try_decorator(timeout=10):
    def decorator(func):
        def wrapper(*args, **kwargs):
            then = time.time()
            while ((time.time() - then) < timeout):
                if (func(*args, **kwargs)):
                    return True
                time.sleep(0.1)
            return False
        return wrapper 
    return decorator

