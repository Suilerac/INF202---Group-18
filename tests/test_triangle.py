import pytest

import math
import numpy as np

from Simulation.triangle import Triangle

expectedValues = {
    "points": [
        np.array([2, 0, 0]),
        np.array([3, 1, 0]),
        np.array([0, 0, 0]),
    ],
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
}

print(expectedValues["edgeLength"])


@pytest.fixture
def triangle():
    return Triangle(expectedValues["points"])


def test_area(triangle):
    assert expectedValues["area"] == triangle.area


def test_centerPoint(triangle):
    assert np.allclose(expectedValues["centerPoint"], triangle.centerPoint)


def test_edgeVectors(triangle):
    for i in range(3):
        assert np.allclose(expectedValues["edgeVectors"][i], triangle.edges[i])


def test_edgeLength(triangle):
    answer = expectedValues["edgeLength"]
    result = triangle.sideLengths
    assert np.allclose(answer, result)


def test_midPoints(triangle):
    for i in range(3):
        # edge midpoints
        m = triangle._calculateEdgeMidPoint(i)
        assert np.allclose(expectedValues["edgeMidPoints"][i], m)


def test_normals(triangle):
    triangle._calculateNormals()
    for i in range(3):
        answer = expectedValues["normals"][i]
        result = triangle.normals[i]
        assert np.allclose(answer, result)
