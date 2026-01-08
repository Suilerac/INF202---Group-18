import numpy as np
from Simulation.triangle import Triangle


points = [
    np.array([2, 0, 0]),
    np.array([3, 1, 0]),
    np.array([0, 0, 0]),
]


t = Triangle(points)

# print("\nArea: ", t.area)
# print("\nCenterPoint: ", t.centerPoint)

# print("\nEdge data:")
# for i in range(3):
#     print("\nEdge: ", i)
#     print("Edge vector: ", t.edges[i])
#     print("Midpoint", t._calculateEdgeMidPoint(i))
#     print("Sidelength", t.sideLengths[i])

t._calculateNormals()
print("\nNormals:")
for normals in t.normals:
    print(normals)
