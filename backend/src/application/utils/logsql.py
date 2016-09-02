import logging


def logsql():
    """
    Enables/disables logging of SQLALchemy sql queries.
    """
    logging.basicConfig()
    logger = logging.getLogger('sqlalchemy.engine')

    if logger.level == logging.NOTSET:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.NOTSET)
