import logging
import sys

__version__ = "0.0.1"

# Initialize a logger for this module.
file_fmt = '%(asctime)s %(name)s: %(levelname)s %(message)s'
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter(file_fmt))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)