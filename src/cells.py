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

    @abstractmethod
    def _calculateArea(self):
        pass

    @abstractmethod
    def getArea(self):
        pass

    @abstractmethod
    def updateOilValue(self):
        pass

    @abstractmethod
    def getOilValue(self):
        pass

    @abstractmethod
    def getFlowValue(self):
        pass

    def addNeighbour(self, ngh):
        self._neighbours.append(ngh)
