import logging

from loguru import logger

import config

class InterceptHandler(logging.InterceptHandler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR"
    }