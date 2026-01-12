import pytest

import math
import numpy as np

from Geometry.triangle import Triangle

expectedValues = {
    "points": np.array([
        [2, 0, 0],
        [3, 1, 0],
        [0, 0, 0],
    ]),
    "centerPoint": np.array([5/3, 1/3, 0]),
    "area": 1.0,
    "edgeLength": np.sqrt(np.array([2, 10, 4])),
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
    "scaledNormals": [
        np.array([1, -1, 0]),
        np.array([-1, 3, 0]),
        np.array([0, -2, 0]),
    ],
}

coords1 = [
    [2, 0, 0],
    [3, 1, 0],
]

coords2 = [
    [3, 1, 0],
    [0, 0, 0],
]

coords3 = [
    [0, 0, 0],
    [2, 0, 0],
]

edgeCoords = [
    coords1,
    coords2,
    coords3,
]


@pytest.fixture
def triangle():
    return Triangle(expectedValues["points"])


def test_area(triangle):
    assert expectedValues["area"] == triangle.area


def test_centerPoint(triangle):
    assert np.allclose(expectedValues["centerPoint"], triangle.centerPoint)


def test_edgeVectors(triangle):
    for i in range(3):
        edgeVector = triangle._calculateEdgeVector(edgeCoords[i])
        assert np.allclose(expectedValues["edgeVectors"][i], edgeVector)


def test_edgeLength(triangle):
    for i in range(3):
        answer = expectedValues["edgeLength"][i]
        edgeVector = triangle._calculateEdgeVector(edgeCoords[i])
        result = triangle._calculateEdgeLength(edgeVector)

        assert result == answer


def test_midPoints(triangle):
    for i in range(3):
        edgeVector = triangle._calculateEdgeVector(edgeCoords[i])
        m = triangle._calculateEdgeMidPoint(edgeCoords[i], edgeVector)
        assert np.allclose(expectedValues["edgeMidPoints"][i], m)


def test_normals(triangle):
    for i in range(3):
        answer = expectedValues["normals"][i]
        result = triangle._calculateNormal(edgeCoords[i])

        assert np.allclose(answer, result)


def test_scaledNormals(triangle):
    for i in range(3):
        answer = expectedValues["scaledNormals"][i]

        result = triangle._calculateScaledNormal(edgeCoords[i])
        assert np.allclose(answer, result)
