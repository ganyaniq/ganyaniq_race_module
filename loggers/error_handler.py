import logging

error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)

handler = logging.FileHandler("error.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

error_logger.addHandler(handler)

def handle_error(e):
    error_logger.error(str(e))
