from .cells import Cell

"""
General attributes of the line class
Oil value is always 0
Lines has a length but no area
"""


class Line(Cell):
    def __init__(self, coordinates):
        super().__init__(coordinates)
        self._flow = [0, 0]

    def _calculateArea(self):
        return 0
