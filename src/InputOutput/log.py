import logging
from pathlib import Path


class Log:
    def __init__(self, logName, logDir='logs'):
        """
        A class for handling logging

        :param logName: Name of logfile
        """
        path = Path(logName)
        self._logName = logName
        self._logDir = logDir
        Path(self._logDir).mkdir(parents=True, exist_ok=True)
        self._logPath = f"{logDir}/{logName}"
        path.parent.mkdir(exist_ok=True)
        # Truncate the log in case it exists to avoid clutter
        with open(self._logPath, 'w') as f:
            f.close()
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
        """
        Ensures that the logger has a file to write to
        """
        if not self._logger.handlers:
            handler = logging.FileHandler(self._logPath)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
