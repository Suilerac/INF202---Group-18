import toml


class TomlParser:
    def __init__(self, configFile: str):
        """
        A class to read and handle values provided by a .toml
        file in relation to the simulation.

        :param configFile: A path string to the toml file
        """
        # Config values
        self._configFile = configFile
        self._nSteps = 0
        self._tEnd = 0
        self._meshName = ""
        self._borders = []
        self._logName = ""
        self._writeFrequency = 0
        self._readConfig()

    @property
    def nSteps(self):
        return self._nSteps

    @property
    def tEnd(self):
        return self._tEnd

    @property
    def meshName(self):
        return self._meshName

    @property
    def borders(self):
        return self._borders

    @property
    def logName(self):
        return self._logName

    @property
    def writeFrequency(self):
        return self._writeFrequency

    @writeFrequency.setter
    def writeFrequency(self, value):
        self._writeFrequency = value

    def _readConfig(self):
        """
        Sets the object properties based on the
        values provided by the toml file
        """
        with open(self._configFile, 'r') as file:
            config = toml.load(file)
        # [settings]
        settings = config.get("settings", {})
        self._nSteps = self._setValueWithNoneHandling(
            "nSteps",
            settings.get("nSteps"),
            int
            )
        self._tEnd = self._setValueWithNoneHandling(
            "tEnd",
            settings.get("tEnd"),
            float
            )

        # [geometry]
        geometry = config.get("geometry", {})
        self._meshName = self._setValueWithNoneHandling(
            "meshName",
            geometry.get("meshName"),
            str
            )
        self._borders = self._setValueWithNoneHandling(
            "borders",
            geometry.get("borders"),
            list
            )

        # [IO]
        io = config.get("IO", {})
        self._logName = io.get("logName", "logfile")
        self._writeFrequency = io.get("writeFrequency", 0)

    def _setValueWithNoneHandling(self, name, value, type):
        if value is None or not isinstance(value, type):
            raise ValueError(
                f"Error parsing config: {name} not given correctly as {type}"
                )
        else:
            return value
