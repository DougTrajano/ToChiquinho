import logging
from src.modeling.logger import setup_logger

def test_setup_logger():
    logger = setup_logger(__name__)
    assert type(logger) == logging.Logger
