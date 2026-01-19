from .cells import Cell


class Line(Cell):
    """
    A class for handeling Line cells
    General attributes of the line class
    Oil value is always 0
    Lines has a length but no area
    """
    def __init__(self, coordinates, pointIDs):
        """
        :param self: coordinates as an np.array for x and y value,
        and pointIDs that make up the line
        """
        super().__init__(coordinates, pointIDs)
        self._flow = [0, 0]

    def _calculateArea(self):
        return 0
