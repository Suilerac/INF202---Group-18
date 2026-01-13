from abc import ABC, abstractmethod


class Cell(ABC):
    """
    An abstract class for handling relevant data of cells
    in the oil simulation
    """
    def __init__(self, coordinates, pointIDs):
        """
        :param coordinates: An array of coordinate vectors
        in the form of numpy arrays
        """
        self._pointIDs = pointIDs
        self._oilValue = 0
        self._update = 0

        self._area = 0
        self._flow = None
        self._neighbours = {}
        self._coordinates = coordinates
        self._centerPoint = sum(self._coordinates) / len(self._coordinates)

    def __str__(self):
        """
        Returns a string in the form [[X Y Z], [X Y Z], ... , [X Y Z]]
        This is to represent the points that make up the cell
        """
        cellStr = '['
        firstLoop = True
        for point in self.coordinates:
            # Only add commas after the first point has been added
            if not firstLoop:
                cellStr += ', '
            cellStr += '['
            # Slicing is used to only add commas after the first number
            cellStr += str(point[0])
            for xyz in point[1:]:
                cellStr += ', '
                cellStr += str(xyz)
            cellStr += ']'
            firstLoop = False
        cellStr += ']'
        return cellStr

    def updateOilValue(self):
        self._oilValue += self._update
        self._update = 0

    def addNeighbour(self, ngh, sharedCoords, flowValue=None):
        self._neighbours[ngh] = [sharedCoords, flowValue]

    def updateFlowToNeighbour(self, ngh, flowValue):
        self._neighbours[ngh][1] = flowValue

    @property
    def neighbours(self):
        return self._neighbours

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def centerPoint(self):
        return self._centerPoint

    @property
    def area(self):
        return self._area

    @property
    def oilValue(self):
        return self._oilValue

    @property
    def flow(self):
        return self._flow

    @property
    def pointIDs(self):
        return self._pointIDs

    @property
    def update(self):
        return self._update

    @update.setter
    def update(self, value):
        self._update = value

    @oilValue.setter
    def oilValue(self, value):
        self._oilValue = value

    @flow.setter
    def flow(self, value):
        self._flow = value

    @abstractmethod
    def _calculateArea(self):
        pass
