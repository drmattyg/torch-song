import time
import sys
import logging
import traceback
from threading import Thread, Event

# Try to run a boolean function for timeout seconds 
def try_decorator(timeout=15):
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

# Run function (as a named string) on every item in iterable in parallel.
# Pass exceptions back to caller
def run_parallel(function_str, iterable):
    runners = []
    events = []

    def worker(item, event):
        try:
            fcn = getattr(item, function_str)
            fcn()
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
            event.set()

    for i in iterable:
        event = Event()
        thread = Thread(target=worker, args=(i,event,))
        thread.setDaemon(True)
        runners.append(thread)
        events.append(event)

    for r in runners:
        r.start()

    done = lambda: any(map(lambda r: not r.isAlive(), runners))
    is_exc = lambda: any(map(lambda e: e.is_set(), events))

    while (not done()):
        if (is_exc()):
            raise Exception('error calling:', function_str)
        time.sleep(.1)

    if (is_exc()):
        raise Exception('error calling:', function_str)

    for r in runners:
        r.join()


