import sys, os
from loguru import logger

# Set up logging
VERBOSE = os.getenv("VERBOSE", "False").lower() in ["true", "1"]
log_level = "INFO" if VERBOSE else "ERROR"
logger.remove()  # Remove default logger configuration
logger.add(sys.stdout, level=log_level, colorize=True, format="<cyan>PANTHEON</cyan>: {message}")
