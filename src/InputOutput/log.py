import logging
from pathlib import Path


class Log:
    def __init__(self, logName):
        path = Path(logName)
        self._logName = logName
        path.parent.mkdir(exist_ok=True)
        self._logger = logging.getLogger(logName)
        self._logger.setLevel(logging.DEBUG)
        self._configureLogger()

    def debug(self, message):
        """
        Log a debug message

        :param message: The message to log
        """
        self._logger.debug(message)

    def info(self, message):
        """
        Log an info message

        :param message: The message to log
        """
        self._logger.info(message)

    def error(self, message):
        """
        Log an error message

        :param message: The message to log
        """
        self._logger.error(message)

    def critical(self, message):
        """
        Log a critical message

        :param message: The message to log
        """
        self._logger.critical(message)

    def _configureLogger(self):
        if not self._logger.handlers:
            handler = logging.FileHandler(self._logName)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
