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
# Run exception_str function on failure
def run_parallel(function_str, iterable, exception_str):
    runners = []
    events = []

    def worker(item, event):
        try:
            fcn = getattr(item, function_str)
            fcn()
        except Exception as e:
            event.set()
            logging.error(e)
            traceback.print_exc()
            try:
                fcn = getattr(item, exception_str)
                fcn()
            except Exception:
                pass

    for i in iterable:
        event = Event()
        thread = Thread(target=worker, args=(i,event,))
        thread.setDaemon(True)
        runners.append(thread)
        events.append(event)

    for r in runners:
        r.start()

    done = lambda: not any(map(lambda r: r.isAlive(), runners))
    is_exc = lambda: any(map(lambda e: e.is_set(), events))

    while (not done()):
        if (is_exc()):
            #raise Exception('error calling:', function_str)
            pass
        time.sleep(.1)

    if (is_exc()):
        #raise Exception('error calling:', function_str)
            pass


    for r in runners:
        r.join()

# sleep for 'secs' but runs 'updater' function every 'update_rate_s'. Return True when complete
# Stop sleep early and return False if 'event'
def interruptable_sleep(secs, event, updater=lambda: None, update_rate_s = .05):
    then = time.time()
    now = time.time()
    while (now - then) < secs:
        updater()
        now = time.time()
        if (event.is_set()):
            return False
        else:
            to_sleep = min(update_rate_s, secs - (now - then))
            time.sleep(max(to_sleep, 0))
    return True

