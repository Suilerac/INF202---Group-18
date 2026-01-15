import meshio
from .cellfactory import CellFactory
from .cells import Cell
from tqdm import tqdm


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
        self._addCellsToList()

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
                "triangle", triangle, self._points
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
                "line", line, self._points
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

    def findNeighboursOf(self, cell: Cell, exclude: int = 0):
        """
        Finds all neighbours of cell

        :param cell: The cell you want to find the neighbours of
        :param exclude: If you want to exclude the first n cells in
            the array of cells, then you can specify n with this parameter
        """
        # Store the point indexes as a set for later comparison
        cellPoints = set(cell.pointIDs)

        # The max amount of neighbours the cell can have
        maxNgh = len(cell.coordinates)

        for ngh in self.cells[exclude:]:
            # Check if all neighbours have already been added
            # That way we can avoid redundant loops
            if len(cell.neighbours) == maxNgh:
                return

            # Store the ngh point indexes as a set for later comparison
            nghPoints = set(ngh.pointIDs)
            # Find the intersection leaving us with the shared point indexes
            sharedPoints = cellPoints & nghPoints
            # If they share exactly two points, then they are neighbours
            if len(sharedPoints) == 2:
                a, b = sharedPoints
                sharedCoords = [self._points[a], self._points[b]]
                cell.addNeighbour(ngh, sharedCoords)
                ngh.addNeighbour(cell, sharedCoords)

    def addAllNeighbours(self):
        """
        Goes through all cells and adds all neighbours for each cell
        """
        # Dict for storing edges and cells together
        # Key: Tuple of two pointIDs
        # Value: Array of cells that have those pointIDs
        edgemap = {}
        for cell in tqdm(self._cells, desc="Finding neighbours"):
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
                        cell.addNeighbour(ngh, sharedCoords)
                        ngh.addNeighbour(cell, sharedCoords)
                # If the edge is not already there, we initialize it
                else:
                    edgemap[edge] = []
                # And add this cell to its value
                edgemap[edge].append(cell)
