from .triangle import Triangle
from .line import Line


class Factory:
    def createCell(type, coordinates):
        """
        A function for creating a new Cell object

        :param type: String of the type of cell. Either "Triangle" or "Line"
        :param coordinates: A list of floats pulled from meshio
        """
        if type == "Triangle":
            return Triangle(coordinates)
        elif type == "Line":
            return Line(coordinates)
