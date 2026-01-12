from .cells import Cell

import numpy as np
from numpy import linalg as la


class Triangle(Cell):
    def __init__(self, coordinates, pointIDs):
        super().__init__(coordinates, pointIDs)
        # vectorized points used for calculations
        self._points = [np.array(coord) for coord in coordinates]

        self._area = self._calculateArea()

    @property
    def edges(self):
        return self._edges

    @property
    def sideLengths(self):
        return self._sideLengths

    @property
    def normals(self):
        return self._normals

    @property
    def scaledNormals(self):
        return self._scaledNormals

    def _calculateArea(self):
        """
        Calculating the area of a triangle

        :param self: Description
        """
        p1 = self._coordinates[0]
        p2 = self._coordinates[1]
        p3 = self._coordinates[2]

        e1 = self._calculateEdgeVector([p1, p2])
        e2 = self._calculateEdgeVector([p1, p3])

        # formula for Area of a triangle given by two vectors
        return 0.5 * la.norm(la.cross(e1, e2))

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
        return la.norm(edgeVector)

    def _calculateNormal(self, coordinates):
        """
        Calculates the normal vectors pointing towards neighbours
        (away from the triangle centerpoint) for every edge in the edges list
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

    def _calculateScaledNormal(self, coordinates):
        # calculateData
        normal = self._calculateNormal(coordinates)
        edgeVector = self._calculateEdgeVector(coordinates)
        edgeLength = la.norm(edgeVector)

        # calulate and store scaled normal
        scaledNormal = normal * edgeLength

        return scaledNormal
