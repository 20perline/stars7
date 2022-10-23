from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stderr,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> {process} [{level}] {name} - <level>{message}</level>",
    level='DEBUG', enqueue=True)
