import os
import sys
import logging

def setup_logger(name: str = __name__) -> logging.Logger:
    """Setup logger.

    Args:
    - name: The name of the logger.
    
    Returns:
    - logger: The logger.
    """
    LOG_LEVEL = int(os.environ.get("SM_LOG_LEVEL", logging.INFO))

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        fmt="%(asctime)s :: %(levelname)s :: %(module)s :: %(funcName)s :: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
