from mesh import Mesh
from cells import Cell

import numpy as np
from numpy import linalg as la

class Triangle(Cell):
    def __init__(self):
        super().__init__()
        self.sideLengths = [0, 0, 0]
        self.points = [None, None, None]
        self.normals = [None, None, None]

    def __str__(self):
        '''
        Prints triangle information
        '''
        pass

    def calculate(self):
        # Vectorize vertecies
        p1 = np.array(Mesh.points[self.pointIDs[0]])
        p2 = np.array(Mesh.points[self.pointIDs[1]])
        p3 = np.array(Mesh.points[self.pointIDs[2]])

        self.points = [p1, p2, p3]

        # centralpint in the shape
        centralPoint = (p1 + p2 + p3) / 3

        # Vectorize edges
        e1 = p2 - p1
        e2 = p3 - p2
        e3 = p1 - p3

        edges = [e1, e2, e3]

        self.sideLengths[0] = np.sqrt(np.dot(e1, e1))
        self.sideLengths[1] = np.sqrt(np.dot(e1, e1))
        self.sideLengths[2] = np.sqrt(np.dot(e1, e1))
        

        # Calculate orthogonal vectors for each edge
        n1 = (np.array(-e1[1], e1[0])) 
        n2 = (np.array(-e2[1], e2[0]))
        n3 = (np.array(-e3[1], e3[0]))

        # normalize the vectors
        n1 = n1 / la.norm(n1)
        n2 = n2 / la.norm(n2)
        n3 = n3 / la.norm(n3)

        self.normals = [n1, n2, n3]

        # correct direction of normal vectors to point out of the triangle
        for i in range(3):
            m = self.points[i] + edges[i] / 2
            center_edge_vector = m - centralPoint
            if (np.dot(self.normals[i], center_edge_vector) < 0): self.normals[i] *= -1

        # Area 
        Area = 0.5 * abs( la.cross(e1, e2))
        

        

        
