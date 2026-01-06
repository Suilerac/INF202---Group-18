from cells import Cell

class Triangle(Cell):
    def __init__(self):
        super().__init__()
        self.sideLengths = [0, 0, 0]
        self.pointIDs = [None, None, None]

    def __str__(self):
        '''
        Prints triangle information
        '''
        pass