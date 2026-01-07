from .cells import Cell


class Line(Cell):
    def __init__(self, coordinates):
        super().__init__(coordinates)

    def _calculateArea(self):
        return 0

    def getArea(self):
        return 0

    def updateOilValue(self, newValue):
        self._oilValue = newValue

    def getOilValue(self):
        return self._oilValue

    def getFlowValue(self):
        return self._flow
