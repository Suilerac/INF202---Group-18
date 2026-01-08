import math
import numpy as np
from Simulation.triangle import Triangle

triangleTestValues = {
    "points": [
        np.array([2, 0, 0]),
        np.array([3, 1, 0]),
        np.array([0, 0, 0]),
    ],
    "centerPoint": np.array([5/3, 1/3, 0]),
    "area": 1.0,
    "edgeLength": np.sqrt(np.array([2, 10, 2])),
    "edgeVectors": [
        np.array([1, 1, 0]),
        np.array([-3, -1, 0]),
        np.array([2, 0, 0]),
    ],
    "edgeMidPoints": [
        np.array([2.5, 0.5, 0]),
        np.array([1.5, 0.5, 0]),
        np.array([1.0, 0, 0]),
    ],
    "normals": [
        np.array([1, -1, 0]) / math.sqrt(2),
        np.array([-1, 3, 0]) / math.sqrt(10),
        np.array([0, -1, 0]),
    ],
}


t = Triangle(triangleTestValues["points"])
print(triangleTestValues["edgeLength"])
# Area
assert triangleTestValues["area"] == t.area
# centerPoint
assert np.allclose(triangleTestValues["centerPoint"], t.centerPoint)

t._calculateNormals()

for i in range(3):
    print("\nEdge: ", i)
    # edge vectors
    assert np.allclose(triangleTestValues["edgeVectors"][i], t.edges[i])
    # edge midpoints
    m = t._calculateEdgeMidPoint(i)
    assert np.allclose(triangleTestValues["edgeMidPoints"][i], m)
    # sidelength
    assert np.allclose(triangleTestValues["edgeLength"][i], t.sideLengths[i])
    # normals
    a = triangleTestValues["normals"][i]
    b = t.normals[i]
    assert np.allclose(triangleTestValues["normals"][i], t.normals[i])


print("\nNormals:")
for normals in t.normals:
    print(normals)
