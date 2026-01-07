from mesh import Mesh
from cells import Cell

import numpy as np
from numpy import linalg as la

class Triangle(Cell):
    def __init__(self, points):
        super().__init__()
        self.points = points

        self.edges = self._calculateEdgeVectors()
        self.normals = [None, None, None]
        self.area = None

    def _calculateArea(self):        
        # Area
        e1 = self.edges[0]
        e2 = self.edges[1] 

        self.area = 0.5 * abs( la.cross(e1, e2))
    
    def _calculateCenterPoint(self):
        # points
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]

        self.centerPoint = (p1 + p2 + p3) / 3

    def _calculateEdgeVectors(self):
        # points
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]
        
        # Vectorize edges
        e1 = p2 - p1
        e2 = p3 - p2
        e3 = p1 - p3

        return [e1, e2, e3]
    
    def _calculateEdgeLengths(self):
        sideLengths = [la.norm(edge) for edge in self.edges]
        return sideLengths

    def _calculateNormals(self):
        # edges
        e1 = self.edges[0]
        e2 = self.edges[1]
        e3 = self.edges[2]


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

        # iterate over every edge
        for i in range(3):
            edgeVectorX = self.edges[0][0] 
            edgeVectorY = self.edges[0][1]

            rotated = [-edgeVectorY, edgeVectorX] # rotate vector 90 degrees counterclockwise (X, Y) -> (-Y, X)
            normal = rotated / la.norm(rotated) # normalising the rotated vector gives the orthonormal

            # Check if the normal points out of the triangle
            m = self.points[i] + self.edges[i] / 2 #midpoint of edge
            centerToMidpointVector = m - self.centralPoint # vector pointing from the center to the midpoint
            
            # check alignment using the dot product. < 0 implies the vector is pointing out
            # of the triangle
            if (np.dot(normal, centerToMidpointVector) < 0): 
                # if it points into the center of the triangle, flip the sign of the normalvector
                normal

            self.normals[i] = normal