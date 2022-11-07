# Load preprocessed dataset
# Traininig model
# Save model
import os
import logging

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

logger.info("Loading dataset")