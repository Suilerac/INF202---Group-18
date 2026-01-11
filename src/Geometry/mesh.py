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

    @property
    def cells(self):
        return self._cells

    @property
    def points(self):
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
        # Appends cell to local cells list
        for triangle in triangles:
            data = triangle.data
            coordinates = [self.points[i] for i in data]
            for coord in coordinates:
                finalObjectCoords = [np.array(c) for c in coord]
                self._cells.append(
                    Factory.createCell("Triangle", finalObjectCoords)
                    )

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
        # Appends cell to local cells list
        for line in lines:
            data = line.data
            coordinates = [self.points[i] for i in data]
            for coord in coordinates:
                finalObjectCoords = [np.array(c) for c in coord]
                self._cells.append(
                    Factory.createCell("Line", finalObjectCoords)
                    )

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

    def _findNeighboursOf(self, cell):
        """
        Finds all neighbours of cell

        :param cell: Cell object
        """
        # Store the coordinates as a list of tuples
        # This is to be able to convert it to a set later
        cellCoords = [tuple(coord.tolist()) for coord in cell.coordinates]
        for ngh in self.cells:
            # Store the ngh coordinates as a list of tuples for the same reason
            nghCoords = [tuple(coord.tolist()) for coord in ngh.coordinates]
            print(f"Neighbour coords: {nghCoords}")
            # Convert both coordinates to sets
            # Check that the amount of elements in the intersection of the two
            # sets is 2
            # If it is, they share two points, and they are neighbours
            sharedCoords = set(cellCoords) & set(nghCoords)
            if len(sharedCoords) == 2:
                cell.addNeighbour(ngh, sharedCoords)
                ngh.addNeighbour(cell, sharedCoords)
