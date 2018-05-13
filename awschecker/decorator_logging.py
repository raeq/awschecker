from functools import wraps
import logging


def logged(loglevel=logging.DEBUG, name=None, message=''):
    """Wrap functions with a logger"""

    def decorate(func):

        loggername = name if name else func.__module__
        logmsg = message if message else func.__module__ + '.'+func.__name__
        logger = logging.getLogger(loggername)

        @wraps(func)
        def wrapper(*args, **kwargs):

            # use the caller's logger
            logger.log(loglevel, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate
