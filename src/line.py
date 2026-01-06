from cells import Cell

class Line(Cell):
    def __init__(self):
        super().__init__()
        self.length = 0
        self.startPointID = None
        self.endPointID = None
    def __str__(self):
        '''
        Prints line information
        '''
        pass