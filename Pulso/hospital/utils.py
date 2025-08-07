from functools import wraps
import time
from django.conf import settings
from pulso.logger import logger

DEBUG = settings.DEBUG

def time_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not DEBUG:
            return func(*args, **kwargs)
        
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            duration = time.perf_counter() - start
            logger.metric(f"{func.__qualname__} executada em {duration:.6f}s")
    return wrapper
