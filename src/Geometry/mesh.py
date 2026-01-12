import meshio
import numpy as np
from .cellfactory import CellFactory
from .cells import Cell


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
        self._factory = CellFactory()
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
            self._cells += self._factory.createCell(
                "Triangle", triangle, self._points
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
            self._cells += self._factory.createCell(
                "Line", line, self._points
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

    def findNeighboursOf(self, cell: Cell) -> list[tuple[Cell, list]]:
        """
        Finds all neighbours of cell

        :param cell: Cell object
        """
        # Store the coordinates as a list of tuples
        # This is to be able to convert it to a set later
        couples = []
        cellPoints = cell.pointIDs
        print("Finding neighbors")
        for ngh in self.cells:
            # Store the ngh coordinates as a list of tuples for the same reason
            nghPoints = ngh.pointIDs
            # Convert both coordinates to sets
            # Check that the amount of elements in the intersection of the two
            # sets is 2
            # If it is, they share two points, and they are neighbours
            sharedPoints = np.intersect1d(cellPoints, nghPoints)
            print("Shared points:" + str(sharedPoints))
            if len(sharedPoints) == 2:
                print("Found neighbor")
                sharedCoords = [self._points[i] for i in sharedPoints]
                couples.append((ngh, sharedCoords))
        return couples
