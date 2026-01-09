import numpy as np
import numpy.linalg as la
import math


class Solver:
    def __init__(self):
        self._initialOilSpatialPoint = np.array[0, 0]

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

        fieldX = y - 0.2 * x
        fieldY = -x
        return np.array([fieldX, fieldY])

    def averageVelocity(a, b):
        return 0.5 * (a + b)
