import logging


def create_logger():
    """Creates and returns a `logging.Logger` object."""
    FORMAT = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger("MinimalPaste")
    logger.setLevel(logging.INFO)
    return logger


logger = create_logger()
