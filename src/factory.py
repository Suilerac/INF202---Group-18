class Factory:
    def createCell(pointIDs, type):
        if type == "Triangle":
            return TriangleCell(pointIDs)
        elif type == "Line":
            return LineCell(pointIDs)
