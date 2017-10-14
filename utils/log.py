import logging
import settings

_loggers = {}

def console():
    if "console" not in _loggers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger = logging.getLogger("console log")
        logger.setLevel(logging.DEBUG if settings.DEBUG_MODE else logging.INFO)
        logger.addHandler(handler)
        _loggers["console"] = logger
    return _loggers["console"]

def file():
    if "file" not in _loggers:
        handler = logging.FileHandler("logs/error.log")
        handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
        logger = logging.getLogger("file log")
        logger.setLevel(logging.WARNING)
        logger.addHandler(handler)
        _loggers["file"] = logger
    return _loggers["file"]
