import meshio
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
        self._x_range = [self._points[:, 0].min(), self._points[:, 0].max()]
        self._y_range = [self._points[:, 1].min(), self._points[:, 1].max()]

        self._cells = []  # List to store all cells as Cell objects
        self._factory = CellFactory()
        self._addCells()

    @property
    def cells(self) -> list[Cell]:
        return self._cells

    @property
    def points(self):
        return self._points

    @property
    def x_range(self):
        return self._x_range

    @property
    def y_range(self):
        return self._y_range

    def addAllNeighbours(self):
        """
        Goes through all cells and adds all neighbours for each cell
        """
        # Dict for storing edges and cells together
        # Key: Tuple of two pointIDs
        # Value: Array of cells that have those pointIDs
        edgemap = {}
        for cell in self._cells:
            pointIDs = cell.pointIDs
            point_amount = len(pointIDs)
            # Goes through each point pair in pointIDs
            for i in range(point_amount):
                p1 = int(pointIDs[i])
                p2 = int(pointIDs[(i + 1) % point_amount])
                edge = tuple(sorted((p1, p2)))  # Key value of edgemap
                # If the edge is already there, it has been added previously
                # along with a cell which is this cell's neighbour
                if edge in edgemap:
                    sharedCoords = [self._points[p1], self._points[p2]]
                    for ngh in edgemap[edge]:

                        scaledNormal = cell.calculateScaledNormal(sharedCoords)
                        cell.addNeighbour(ngh, scaledNormal)
                        ngh.addNeighbour(cell, -scaledNormal)
                # If the edge is not already there, we initialize it
                else:
                    edgemap[edge] = []
                # And add this cell to its value
                edgemap[edge].append(cell)

    def _addCells(self):
        """
        Creates all cell objects and adds them to the cell list
        """
        for cell, index in self._findCellIndexes().items():
            self._cells += self._factory.createCell(
                cell.type, self._mesh.cells[index], self._points
            )

    def _findCellIndexes(self):
        """
        Finds the indexes of cells supported by the cellFactory
        """
        indexes = {}
        i = 0
        for cell in self._mesh.cells:
            if cell.type in self._factory.types:
                indexes[cell] = i
            i += 1
        return indexes
