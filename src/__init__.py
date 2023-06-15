import os
import src.settings
from loguru import logger


def start_app() -> None:
	os.system(settings.STARTING_COMMAND)


def logger_init() -> None:
	for level in src.settings.LOGGING_LEVELS:
		logger.add(
			src.settings.ERRORS_OUTPUT_FILE,
			level=level,
			format=src.settings.LOGGING_FORMAT,
			rotation="1 MB",
			compression="zip"
		)

