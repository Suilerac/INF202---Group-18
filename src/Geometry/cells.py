from abc import ABC, abstractmethod
import numpy as np
import numpy.linalg as la


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
        self._oilDensity = 0
        self._update = 0
        # geometric attributes
        self._velocity = None
        self._area = 0
        self._coordinates = coordinates
        self._centerPoint = sum(coordinates) / len(coordinates)
        self._neighbours = {}
        # flag for analysis
        self._inFishingGround = False

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

    @abstractmethod
    def _calculateArea(self):
        pass

    @property
    def area(self):
        return self._area

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def neighbours(self):
        return self._neighbours

    @property
    def centerPoint(self):
        return self._centerPoint

    @property
    def pointIDs(self):
        return self._pointIDs

    @property
    def oilDensity(self):
        return self._oilDensity

    @oilDensity.setter
    def oilDensity(self, value):
        self._oilDensity = value

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    @property
    def update(self):
        return self._update

    @update.setter
    def update(self, value):
        self._update = value

    @property
    def inFishingGround(self):
        return self._inFishingGround

    @inFishingGround.setter
    def inFishingGround(self, value: bool):
        self._inFishingGround = value

    def updateOilDensity(self):
        """
        Add the update value to the cells oildensity
        """
        self._oilDensity += self._update
        # resets the update value
        self._update = 0

    def addNeighbour(self, ngh, scaledNormal):
        """
        registers a neighbour the neighbours dictionary together
        with the related scalednormal pointing out from main cell

        :param ngh: Neighbour cell object
        :param scaledNormal: scalednormal pointing from cell to ngh
        """
        self._neighbours[ngh] = scaledNormal

    def calculateScaledNormal(self, coordinates):
        """
        Calculates the scalednormal vectors pointing towards neighbours
        (away from the triangle centerpoint) for every edge in the edges list

        :param coordinates: A list of the endpoints to the edge related to
        the scalednormal you desire to calculate
        """
        # calculateData
        normal = self._calculateNormal(coordinates)
        edgeVector = self._calculateEdgeVector(coordinates)
        edgeLength = la.norm(edgeVector)

        # calulate and store scaled normal
        scaledNormal = normal * edgeLength

        return scaledNormal[:2]

    def _calculateEdgeVector(self, coordinates):
        """
        Creates vectors between every point in the triangle
        """
        # points
        p1 = np.array(coordinates[0])
        p2 = np.array(coordinates[1])

        # Vectorize edges
        return p2 - p1

    def _calculateEdgeMidPoint(self, coordinates, edgeVector):
        """
        Calculates the midpoints of a line / edge

        :param edge: index refering to a edgevector in the edges list
        """
        p1 = np.array(coordinates[0])

        return p1 + edgeVector / 2

    def _calculateEdgeLength(self, edgeVector):
        """
        Calulates the length for an edge

        :param edgeVector: vector between two points
        of a cell given as a np array
        """
        return la.norm(edgeVector)

    def _calculateNormal(self, coordinates):
        """
        Calculates the normal vector pointing towards a neighbour
        (away from the triangle centerpoint) for a related edge connecting
        the two cells

        :param coordinates: A list of the endpoints to the edge related to
        the normal you desire to calculate
        """

        # decompose edge vector
        edgeVector = self._calculateEdgeVector(coordinates)

        x = edgeVector[0]
        y = edgeVector[1]

        # rotate vector 90 degrees counterclockwise (X, Y, 0) -> (-Y, X, 0)
        rotated = np.array([-y, x, 0])

        # normalising the rotated vector gives the orthonormal
        normal = rotated / la.norm(rotated)

        # vector pointing from the center to the midpoint
        midPoint = self._calculateEdgeMidPoint(coordinates, edgeVector)
        centerToMidpointVector = midPoint - self._centerPoint

        # check alignment using the dot product.
        # (0 < Alignment) implies the vector is pointing out
        # of the triangle
        alignment = np.dot(normal, centerToMidpointVector)

        if (alignment < 0):
            # if it points into the center of the triangle,
            # flip the sign of the normalvector
            normal *= -1

        return normal
