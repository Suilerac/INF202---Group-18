import pytest
from Geometry.triangle import Triangle
import math
import numpy as np

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


@pytest.fixture
def triangle():
    """
    Returns triangle object
    """
    return Triangle(
        np.array([
            [2, 0, 0],
            [3, 1, 0],
            [0, 0, 0],
        ]),
        []
    )


def test_updateOilDensity(triangle):
    """
    Tests that oilDensity updates as expected
    """
    velocityIn = 10
    triangle.update = velocityIn
    triangle.updateOilDensity()
    assert triangle.oilDensity == velocityIn


@pytest.mark.parametrize("expectedArea", [
    (1.0),
])
def test_area(triangle, expectedArea):
    """
    Tests that area calculation returns expected value
    """
    assert triangle.area == expectedArea


@pytest.mark.parametrize("expectedCenterPoint", [
    (np.array([5/3, 1/3, 0])),
])
def test_centerPoint(triangle, expectedCenterPoint):
    """
    Tests that centerpoint calculation returns expected value
    """
    assert np.allclose(triangle.centerPoint, expectedCenterPoint)


@pytest.mark.parametrize("edgeCoords, expectedEdgeVectors", [
    (coords1, np.array([1, 1, 0])),
    (coords2, np.array([-3, -1, 0])),
    (coords3, np.array([2, 0, 0])),
])
def test_edgeVectors(triangle, edgeCoords, expectedEdgeVectors):
    """
    Tests that edge vector calculation returns expected value
    """
    result = triangle._calculateEdgeVector(edgeCoords)
    assert np.allclose(result, expectedEdgeVectors)


@pytest.mark.parametrize("edgeCoords, expectedEdgeLength", [
    (coords1, math.sqrt(2)),
    (coords2, math.sqrt(10)),
    (coords3, 2),
])
def test_edgeLength(triangle, edgeCoords, expectedEdgeLength):
    """
    Tests that edge length calculation returns expected value
    """
    edgeVector = triangle._calculateEdgeVector(edgeCoords)
    result = triangle._calculateEdgeLength(edgeVector)
    assert result == expectedEdgeLength


@pytest.mark.parametrize("edgeCoords, expectedMidpoints", [
    (coords1, np.array([2.5, 0.5, 0])),
    (coords2, np.array([1.5, 0.5, 0])),
    (coords3, np.array([1.0, 0, 0])),
])
def test_midPoints(triangle, edgeCoords, expectedMidpoints):
    """
    Tests that midpoint calculation returns expected value
    """
    edgeVector = triangle._calculateEdgeVector(edgeCoords)
    result = triangle._calculateEdgeMidPoint(edgeCoords, edgeVector)
    assert np.allclose(result, expectedMidpoints)


@pytest.mark.parametrize("edgeCoords, expectedNormals", [
    (coords1, np.array([1, -1, 0]) / math.sqrt(2)),
    (coords2, np.array([-1, 3, 0]) / math.sqrt(10)),
    (coords3, np.array([0, -1, 0])),
])
def test_normals(triangle, edgeCoords, expectedNormals):
    """
    Tests that normal calculation returns expected value
    """
    result = triangle._calculateNormal(edgeCoords)
    assert np.allclose(result, expectedNormals)


@pytest.mark.parametrize("edgeCoords, expectedScaledNormals", [
    (coords1, np.array([1, -1])),
    (coords2, np.array([-1, 3])),
    (coords3, np.array([0, -2])),
])
def test_scaledNormals(triangle, edgeCoords, expectedScaledNormals):
    """
    Tests that scaled normal calculation returns expected value
    """
    result = triangle.calculateScaledNormal(edgeCoords)
    assert np.allclose(result, expectedScaledNormals)
