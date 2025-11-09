import logging

logger = logging.getLogger("update_logger")
logger.setLevel(logging.INFO)

handler = logging.FileHandler("update.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def log_update(message):
    logger.info(message)
