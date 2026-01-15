import argparse
import os


class commandlineParser:
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._folder = None
        self._config_file = None
        self._findAll = False
        self._addArguments()
        self._parse()

    def getConfigList(self):
        """
        Get a list of all config paths requested by the user
        """
        configs = []
        path = ''
        # If there is a folder, add a "folder/" prefix
        # If there is no folder, it won't have a prefix
        if len(self._folder > 0):
            path = f"{self._folder}/"
        # Gets all config files in folder if it is supposed to
        if self._findAll:
            configFiles = os.listdir(self._folder)
            configs.append(
                f"{path}{file}" for file
                in configFiles if ".toml" in file
                )
        # Gets specific config file if it's supposed to
        else:
            file = f"{path}{self._config_file}"
            configs.append(file)
        return configs

    @property
    def folder(self):
        return self._folder

    @property
    def config_file(self):
        return self._config_file

    @property
    def findAll(self):
        return self._findAll

    def _addArguments(self):
        self._parser.add_argument("--find_all", action='store_true')
        self._parser.add_argument("-f", "--folder", nargs=1, default='')
        self._parser.add_argument("-c", "--config_file",
                                  nargs=1, default="input.toml")

    def _parse(self):
        args = self._parser.parse_args()
        self._folder = args.folder
        self._config_file = args.config_file
        self._findAll = args.config_file
