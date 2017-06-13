import time

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


def log_decorator(log_enabled):
    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            if log_enabled:
                print("Calling Function: " + func.__name__)
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator


