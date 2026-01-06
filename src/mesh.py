import meshio
from factory import Factory


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
        self.mesh = meshio.read(meshFile)
        self.points = self.mesh.points
        self.cells = []  # List to store all cells as Cell objects
        self._addCellsToList()

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
        triangles = self.mesh.cells[1]
        for triangle in triangles:
            self.cells.append(Factory.createCell("Triangle", triangle.data))

    def _addLines(self):
        """
        Creates LineCell objects of the border cells and adds
        them to the list.
        """
        lines = self.mesh.cells[0]
        for line in lines:
            self.cells.append(Factory.createCell("Line", line.data))
