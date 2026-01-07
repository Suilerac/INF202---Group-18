from cells import Cell

import numpy as np
from numpy import linalg as la


class Triangle(Cell):
    def __init__(self, points):
        super().__init__()
        self.points = points

        # order of these calculations matter
        self.centerPoint = self._calculateCenterPoint()

        self.edges = self._calculateEdgeVectors()
        self.sideLengths = self._calculateSideLengths()

        self.area = self._calculateArea()
        self.normals = [None, None, None]

    def _calculateArea(self):
        """
        Calculating the area of a triangle

        :param self: Description
        """
        e1 = self.edges[0]
        e2 = self.edges[1]

        # formula for Area of a triangle given by two vectors
        self.area = 0.5 * abs(la.cross(e1, e2))

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
        sideLengths = [la.norm(edge) for edge in self.edges]
        return sideLengths

    def _calculateEdgeMidPoint(self, edgeIndex):
        """
        Calculates the midpoints of a line / edge

        :param edge: index refering to a edgevector in the edges list
        """
        return self.points[edgeIndex] + self.edges[edgeIndex] / 2

    def _calculateNormals(self):
        """
        Calculates the normal vectors pointing towards neighbours
        (away from the triangle centerpoint) for every edge in the edges list
        """

        # iterate over every edge in edges
        for i in range(3):
            # decompose edge vector
            x = self.edges[i][0]
            y = self.edges[i][1]

            # rotate vector 90 degrees counterclockwise (X, Y) -> (-Y, X)
            rotated = np.array(-y, x)

            # normalising the rotated vector gives the orthonormal
            normal = rotated / la.norm(rotated)

            # vector pointing from the center to the midpoint
            midPoint = self._calculateEdgeMidPoint(i)
            centerToMidpointVector = midPoint - self.centralPoint

            # check alignment using the dot product.
            # S < 0 implies the vector is pointing out
            # of the triangle
            alignment = np.dot(normal, centerToMidpointVector)
            if (alignment < 0):
                # if it points into the center of the triangle,
                # flip the sign of the normalvector
                normal *= -1

            self.normals[i] = normal
