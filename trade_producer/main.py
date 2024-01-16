import logging

from src.main import run
from src.utils import initialize_logger

initialize_logger()

logger = logging.getLogger()
logger.info('Starting trade producer...')
run()
