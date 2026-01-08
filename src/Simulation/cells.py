from abc import ABC, abstractmethod


class Cell(ABC):
    """
    An abstract class for handling relevant data of cells
    in the oil simulation
    """
    def __init__(self, coordinates):
        """
        :param coordinates: An array of coordinate vectors
        in the form of numpy arrays
        """
        self._oilValue = 0
        self._area = 0
        self._flow = []
        self._neighbours = []
        self._coordinates = coordinates

    def __str__(self):
        return str(self._coordinates)

    @property
    def neighbours(self):
        return self._neighbours

    @property
    def coordinates(self):
        return self._coordinates

    @abstractmethod
    def _calculateArea(self):
        pass

    def getArea(self):
        return self._area

    def updateOilValue(self, value):
        self._oilValue = value

    def getOilValue(self):
        return self._oilValue

    def getFlowValue(self):
        return self._flow

    def addNeighbour(self, ngh):
        self._neighbours.append(ngh)
