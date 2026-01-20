import math
import numpy as np
from Geometry.line import Line
la = np.linalg


class Solver:
    def __init__(self, initialOilPoint=np.array([0.35, 0.45])):
        self._initialOilSpatialPoint = initialOilPoint
        self._fieldIsTimeDependent = self._vectorFieldIsTimedependent()

    def initalOil(self, position):
        """
        calulating initial oil value from a position vector

        :param position: A numpy array with two elements (x, y)
        """
        distance = la.norm(position - self._initialOilSpatialPoint)
        oilDensity = math.exp(- (distance * distance / 0.01))
        return oilDensity

    def vectorField(self, position, t=0):
        """
        calculating the vector field from a position vector

        :param position: A numpy array with at least two elements (x, y)
        """
        x = position[0]
        y = position[1]

        fieldX = y - 0.2 * x
        fieldY = -x
        return np.array([fieldX, fieldY])

    def _vectorFieldIsTimedependent(self):
        """
        Checks if the partial derivative of the vectorField with
        respect to time equals [0, 0].
        If it is true then we can use the faucet optimisation
        """
        testPos = np.array([1, 1])
        for t in range(10):
            vI = self.vectorField(testPos, t)
            vF = self.vectorField(testPos, t + 1)

            if la.norm(vI - vF) != 0:
                return True

        return False

    def _averageVelocity(self, velocityA, velocityB):
        return 0.5 * (velocityA + velocityB)

    def flux(self, mainCell, nghCell, averageVelocity, scaledNormal):
        if isinstance(mainCell, Line) or isinstance(nghCell, Line):
            return 0

        dot = np.dot(averageVelocity, scaledNormal)
        if (0 <= dot):
            return mainCell.oilDensity * dot
        else:
            return nghCell.oilDensity * dot
