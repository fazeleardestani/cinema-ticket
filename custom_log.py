"""Configures the application logger to write to cinematicket.log."""
import logging

FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('cinematicket.log')
file_formatter = logging.Formatter(FORMAT)
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)



