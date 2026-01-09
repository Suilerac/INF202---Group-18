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
        self._neighbours = {}
        self._coordinates = coordinates

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

    def _edgeIdFromCoords(self, coords):
        p1 = tuple(round(component / 1e-10) for component in coords[0])
        p2 = tuple(round(component / 1e-10) for component in coords[1])

        return tuple(sorted((p1, p2)))

    def addNeighbour(self, ngh):
        self._neighbours[ngh] = 0

    @property
    def neighbours(self):
        return self._neighbours

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def area(self):
        return self._area

    @property
    def oilValue(self):
        return self._oilValue

    @property
    def flow(self):
        return self._flow

    @oilValue.setter
    def oilValue(self, value):
        self._oilValue = value

    @abstractmethod
    def _calculateArea(self):
        pass
