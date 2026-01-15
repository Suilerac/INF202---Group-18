import logging


class Log:
    def __init__(self, logName):
        self._logName = logName

    def debug(self, message):
        """
        Log a debug message

        :param message: The message to log
        """
        self._configureLogger()
        logging.debug(message)

    def info(self, message):
        """
        Log an info message

        :param message: The message to log
        """
        self._configureLogger()
        logging.info(message)

    def error(self, message):
        """
        Log an error message

        :param message: The message to log
        """
        self._configureLogger()
        logging.error(message)

    def critical(self, message):
        """
        Log a critical message

        :param message: The message to log
        """
        self._configureLogger()
        logging.critical(message)

    def _configureLogger(self):
        """
        Configures the logger for the current log file.
        This is done in every method because logging is global.
        This is problematic if we're dealing with multiple log files at once.
        That happens when running multiple simulations,
        as we utilize multiprocessing.
        As such we need to reset it to the correct file every time.
        """
        logging.basicConfig(
            filename=self._logName,
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
