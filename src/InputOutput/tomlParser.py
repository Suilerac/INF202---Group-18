import toml


class TomlParser:
    def __init__(self, configFile: str):
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
        with open(self._configFile, 'r') as file:
            config = toml.load(file)
        settings = config.get("settings", {})
        self._nSteps = settings.get("nSteps", 500)
        self._tEnd = settings.get("tEnd", 0.5)

        geometry = config.get("geometry", {})
        self._meshName = geometry.get("meshName", "meshes/bay.msh")
        self._borders = geometry.get("borders", [[0, 0.45], 0, 0.2])

        io = config.get("IO", {})
        self._logName = io.get("logName", "log")
        self._writeFrequency = io.get("writeFrequency", False)
