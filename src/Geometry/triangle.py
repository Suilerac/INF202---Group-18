from .cells import Cell
from numpy import linalg as la


class Triangle(Cell):
    """
    A class for handeling triangle cells
    """
    def __init__(self, coordinates, pointIDs):
        """
        :param coordinates: coordinates as an np.array for x and y value
        :param pointIDs: pointIDs that make up the triangle
        """
        super().__init__(coordinates, pointIDs)

        self._area = self._calculateArea()

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
