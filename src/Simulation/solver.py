import math
import numpy as np
import numpy.linalg as la
from Geometry.line import Line


class Solver:
    def __init__(self, initialOilPoint=np.array([0.35, 0.45])):
        """
        Solver for handling physics

        :param initialOilPoint: numpy array containing at
        least two elements [x, y...], representing the source for the oil
        spillage (optional parameter)
        """
        self._initialOilSpatialPoint = initialOilPoint[:2]
        self._fieldIsTimeDependent = self._vectorFieldIsTimedependent()

    def initalOil(self, position):
        """
        calulating initial oildensity from a position vector

        :param position: A numpy array with two elements (x, y)
        """
        distance = la.norm(position - self._initialOilSpatialPoint)
        oilDensity = math.exp(- (distance * distance / 0.01))
        return oilDensity

    def vectorField(self, position, t=0):
        """
        calculating the vector field from a position vector

        :param position: A numpy array with at least two elements (x, y)
        :param t: a float value for elapsed time (optional)
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
        """
        Calculates the average between two velocity vectors of the
        same size. Could have used np.mean but a descriptive method is better
        for readability

        :param velocityA: np array [x, y...]
        :param velocityB: np array [x, y...]

        :rtype: np array [x, y...]
        """
        return 0.5 * (velocityA + velocityB)

    def flux(self, mainCell, nghCell, averageVelocity, scaledNormal):
        """
        Calculates the flux out over a cell edge shared by a main cell and a
        neighbouring cell. The flux is related to the perspective
        of the main cell.

        :param mainCell: cell object
        :param nghCell: cell object
        :param averageVelocity: average velocity between the two cells
        :param scaledNormal: the scaledNormal outgoing from the main cell
        """
        # this is not necessary for functionality as all line cells are skipped
        # but it makes the flux method more user friendly
        if isinstance(mainCell, Line) or isinstance(nghCell, Line):
            return 0

        # alignment
        dot = np.dot(averageVelocity, scaledNormal)

        if (0 <= dot):
            # ougoting flux
            return mainCell.oilDensity * dot
        else:
            # incoming flux
            return nghCell.oilDensity * dot
