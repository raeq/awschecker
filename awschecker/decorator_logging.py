from functools import wraps, partial
from pprint import pprint
from os import path
import logging


def logged(func, loglevel=logging.DEBUG, name=None, message=''):
    """Wrap functions with a logger"""

    def decorate(func):

        loggername = name if name else func.__module__
        logmsg = message if message else func.__module__ +'.'+func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):

            logger = logging.getLogger(loggername)
            logger.log(loglevel, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate
