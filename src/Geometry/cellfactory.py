from .triangle import Triangle
from .line import Line
import numpy as np


class CellFactory:
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
        for coord in coordinates:
            finalObjectCoords = np.array(coord)
            if type == "Triangle":
                cells.append(Triangle(finalObjectCoords))
            elif type == "Line":
                cells.append(Line(finalObjectCoords))
        return cells
