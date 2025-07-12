"""Configures the application logger to write to cinematicket.log."""
import logging

FORMAT = ('%(asctime)s - %(levelname)s \n\t'
          '--> %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('cinematicket.log')
file_formatter = logging.Formatter(FORMAT)
file_handler.setFormatter(file_formatter)

stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter(FORMAT)
stream_handler.setFormatter(stream_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)



