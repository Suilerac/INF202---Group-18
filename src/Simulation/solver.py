import math
import numpy as np
from src.Geometry.line import Line
la = np.linalg


class Solver:
    def __init__(self, initialOilPoint=np.array([0.35, 0.45])):
        self._initialOilSpatialPoint = initialOilPoint

    def initalOil(self, position):
        """
        calulating initial oil value from a position vector

        :param position: A numpy array with two elements (x, y)
        """
        distance = la.norm(position - self._initialOilSpatialPoint)
        oilValue = math.exp(- (distance * distance / 0.01))
        return oilValue

    def vectorField(self, position):
        """
        calculating the vector field from a position vector

        :param position: A numpy array with at least two elements (x, y)
        """
        x = position[0]
        y = position[1]

        fieldX = y - 0.2 * y
        fieldY = -x
        return np.array([fieldX, fieldY])

    def _averageVelocity(self, cellA, cellB):
        vA = cellA.flow
        vB = cellB.flow
        return 0.5 * (vA + vB)

    def calculateFlowValue(self, cellA, cellB, sharedCoordinates):
        if isinstance(cellB, Line):
            return 0
        """
        Calculates a scalar value that gives the flow from cell A to cell B.
        This is calculated from the dot product of the average velocity
        between cellA and cellB and the scaled normal pointing
        from cellA to cellB.

        parameters:
            cellA: cell object,
            cellB: cell object,
            edgeID: tuple key calculated by cell.
        """

        # Since the vector field is constant at a given position.
        # Therefore the average velocity between cells is constant as well
        averageVelocity = self._averageVelocity(cellA, cellB)

        # The scaled normals of the shared edge between cellA and cellB
        # are parallell to each other, with opposite direction.
        # They have the same lenght s the relation between them is given as
        # "scaledNormalA = - scaledNormalB"
        scaledNormal = cellA._calculateScaledNormal(sharedCoordinates)

        # since both the averageVelocity and the scaledNormal is constant
        # we only have to calculate this value once during the simulation.
        # this saves a lot of time
        return np.dot(averageVelocity, scaledNormal)

    def flux(self, cellA, cellB, flowValue):
        # the flowvalue is the dot product of
        # the average velocity between two neighbours
        # and the scaled normal of the shared edge
        if (0 < flowValue):
            return cellA.oilValue * flowValue
        else:
            return cellB.oilValue * flowValue
