import os

from loguru import logger

import src.settings


def start_app() -> None:
	"""
	Запуск сервера
	"""
	os.system(settings.STARTING_COMMAND)


def logger_init() -> None:
	"""
	Использую loguru для дополнительного логирования
	"""
	for level in src.settings.LOGGING_LEVELS:
		logger.add(
			src.settings.ERRORS_OUTPUT_FILE,
			level=level,
			format=src.settings.LOGGING_FORMAT,
			rotation="1 MB",
			compression="zip"
		)

