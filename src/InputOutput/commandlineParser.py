import argparse
import os


class CommandlineParser:
    def __init__(self):
        """
        A class for handling the command line arguments
        for the simulation.
        """
        self._parser = argparse.ArgumentParser()
        self._folder = None
        self._config_file = None
        self._findAll = False
        self._configs = []
        self._addArguments()

    @property
    def configs(self):
        return self._configs

    @property
    def folder(self):
        return self._folder

    @property
    def config_file(self):
        return self._config_file

    @property
    def findAll(self):
        return self._findAll

    def setConfigList(self):
        """
        Get a list of all config paths requested by the user
        """
        path = ''
        # If there is a folder, add a "folder/" prefix
        # If there is no folder, it won't have a prefix
        files = []
        if len(self._folder) > 0:
            path = f"{self._folder}/"
            files = os.listdir(self._folder)
        else:
            files = os.listdir()
        # Gets all config files in folder if it is supposed to
        if self._findAll:
            self._configs = [
                f"{path}{file}" for file in files if file.endswith(".toml")
                ]
            if f"{path}pyproject.toml" in self._configs:
                self._configs.remove(f"{path}pyproject.toml")
        # Gets specific config file if it's supposed to
        else:
            file = f"{path}{self._config_file}"
            self._configs.append(file)

        # Error handling
        if len(self._configs) == 0:
            raise FileExistsError("Found no files as specified")
        # This obviously doesn't cover all possible cases, but if someone
        # wants to overwrite system32 or something, be my guest
        dontOverwrite = ["src", "tests", "examples", "temp", "configs"]
        for config in self._configs:
            if not os.path.isfile(config):
                raise FileNotFoundError(f"Found no file {config}")
            file = config.split('/')[-1]
            name = file.split('.')[0]
            if name in dontOverwrite:
                raise PermissionError(f"{config} can't overwrite {name}")

    def parse(self):
        """
        Parses the arguments and sets the class properties accordingly
        """
        args = self._parser.parse_args()
        self._folder = args.folder
        self._config_file = args.config_file
        self._findAll = args.find_all

    def _addArguments(self):
        """
        Adds all the command line arguments for parsing
        """
        self._parser.add_argument("--find_all", action='store_true')
        self._parser.add_argument("-f", "--folder", default='')
        self._parser.add_argument("-c", "--config_file", default="input.toml")
