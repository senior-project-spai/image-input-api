import logging
import sys

# Create logger
logger = logging.getLogger("app")

# Create handler
handler = logging.StreamHandler()

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)
logger.setLevel(logging.INFO)