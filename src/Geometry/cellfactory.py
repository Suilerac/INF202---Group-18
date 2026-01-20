from .triangle import Triangle
from .line import Line
import numpy as np


class CellFactory:
    def __init__(self):
        """
        A factory class for cell creation
        """
        self._types = {
            "line": Line,
            "triangle": Triangle
            }

    @property
    def types(self):
        return self._types

    def createCell(self, type, cell, points):
        """
        A function for creating a list of new Cell objects based
        on meshio data

        :param type: String of the type of cell. Either "Triangle" or "Line"
        :param cell: Cell from meshio mesh
        :param points: Full points list from meshio
        """
        cells = []
        data = cell.data
        coordinates = [points[i] for i in data]
        for i in range(len(coordinates)):
            finalObjectCoords = np.array(coordinates[i])
            pointIDs = data[i]
            cells.append(self._types[type](finalObjectCoords, pointIDs))
        return cells
