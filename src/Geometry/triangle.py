from .cells import Cell

import numpy as np
from numpy import linalg as la


class Triangle(Cell):
    def __init__(self, coordinates):
        super().__init__(coordinates)
        # vectorized points used for calculations
        self._points = [np.array(coord) for coord in coordinates]

        # order of these calculations matter
        self._centerPoint = self._calculateCenterPoint()

        self._edges = self._calculateEdgeVectors()
        self._sideLengths = self._calculateSideLengths()

        self._area = self._calculateArea()
        self._normals = [None, None, None]

    @property
    def centerPoint(self):
        return self._centerPoint

    @property
    def edges(self):
        return self._edges

    @property
    def sideLengths(self):
        return self._sideLengths

    @property
    def normals(self):
        return self._normals

    def _calculateArea(self):
        """
        Calculating the area of a triangle

        :param self: Description
        """
        e1 = self._edges[0]
        e2 = self._edges[1]

        # formula for Area of a triangle given by two vectors
        return 0.5 * la.norm(la.cross(e1, e2))

    def _calculateCenterPoint(self):
        """
        Calulates the centerpoint of the triangle
        """
        # points
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]

        # centerpint is the average of the three
        return (p1 + p2 + p3) / 3

    def _calculateEdgeVectors(self):
        """
        Creates vectors between every point in the triangle
        """
        # points
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]

        # Vectorize edges
        e1 = p2 - p1
        e2 = p3 - p2
        e3 = p1 - p3

        return [e1, e2, e3]

    def _calculateSideLengths(self):
        """
        Calulate the side lengths for every edge vector in the edges list
        """
        sideLengths = [la.norm(edge) for edge in self._edges]
        return sideLengths

    def _calculateEdgeMidPoint(self, edgeIndex):
        """
        Calculates the midpoints of a line / edge

        :param edge: index refering to a edgevector in the edges list
        """
        return self.points[edgeIndex] + self._edges[edgeIndex] / 2

    def _calculateNormals(self):
        """
        Calculates the normal vectors pointing towards neighbours
        (away from the triangle centerpoint) for every edge in the edges list
        """

        # iterate over every edge in edges
        for i in range(3):
            # decompose edge vector
            x = self._edges[i][0]
            y = self._edges[i][1]

            # rotate vector 90 degrees counterclockwise (X, Y) -> (-Y, X)
            rotated = np.array([-y, x, 0])

            # normalising the rotated vector gives the orthonormal
            normal = rotated / la.norm(rotated)

            # vector pointing from the center to the midpoint
            midPoint = self._calculateEdgeMidPoint(i)
            centerToMidpointVector = midPoint - self._centerPoint

            # check alignment using the dot product.
            # (0 < Alignment) implies the vector is pointing out
            # of the triangle
            alignment = np.dot(normal, centerToMidpointVector)

            if (alignment < 0):
                # if it points into the center of the triangle,
                # flip the sign of the normalvector
                normal *= -1

            self._normals[i] = normal
