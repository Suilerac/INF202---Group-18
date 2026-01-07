import meshio
import numpy as np
from .factory import Factory


class Mesh:
    def __init__(self, meshFile):
        """
        A class to keep track of relevant data in a computational mesh.
        It uses meshio to read the mesh, and then stores the relevant data.

        The main difference from this class and just the return value of
        meshio.read() is the usage of our custom Cell class to keep track
        of cells.

        :param meshFile: String of the file name for the .msh file
        """
        self._mesh = meshio.read(meshFile)
        self._points = self._mesh.points
        self._cells = []  # List to store all cells as Cell objects
        self._addCellsToList()

    def getCells(self):
        return self._cells

    def getPoints(self):
        return self._points

    def _addCellsToList(self):
        """
        Adds all cells to the list
        """
        self._addTriangles()
        self._addLines()

    def _addTriangles(self):
        """
        Creates TriangleCell objects of the triangle cells
        and adds them to the list
        """
        triangles = []
        for i in self._findTriangleIndexes():
            triangles.append(self._mesh.cells[i])
        # Finds and vectorizes the coordinates for the cell
        # Creates cell
        # Appends cell to cells local cells list
        for triangle in triangles:
            data = triangle.data
            coordinates = [np.array(self._points[i]) for i in data]
            self._cells.append(Factory.createCell("Triangle", coordinates))

    def _addLines(self):
        """
        Creates LineCell objects of the border cells and adds
        them to the list.
        """
        lines = []
        for i in self._findLineIndexes():
            lines.append(self._mesh.cells[i])
        # Finds and vectorizes the coordinates for the cell
        # Creates cell
        # Appends cell to cells local cells list
        for line in lines:
            data = line.data
            coordinates = np.array([self._points[i] for i in data])
            self._cells.append(Factory.createCell("Line", coordinates))

    def _findTriangleIndexes(self):
        """
        Finds the indexes of triangle cells in a meshio cell list
        """
        indexes = []
        meshioCellList = self._mesh.cells
        i = 0
        for _ in meshioCellList:
            if meshioCellList[i].type == "triangle":
                indexes.append(i)
            i += 1
        return indexes

    def _findLineIndexes(self):
        """
        Finds the indexes of line cells in a meshio cell list
        """
        indexes = []
        meshioCellList = self._mesh.cells
        i = 0
        for _ in meshioCellList:
            if meshioCellList[i].type == "line":
                indexes.append(i)
            i += 1
        return indexes
