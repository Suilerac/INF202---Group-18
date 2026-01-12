import pytest
import numpy as np
from Geometry.mesh import Mesh
from Geometry.cells import Cell


@pytest.fixture
def mesh():
    return Mesh("meshes/simple_mesh.msh")


# Assert that the lists of datapoints aren't left empty
def test_list_filling(mesh):
    assert len(mesh.cells) > 0
    assert len(mesh.points) > 0


# Assert that correct indexes are found
def test_index_search(mesh):
    assert mesh._findTriangleIndexes() == [8]
    assert mesh._findLineIndexes() == [4, 5, 6, 7]


def test_points(mesh):
    assert isinstance(mesh.cells[0].coordinates, np.ndarray)


def test_neighbours(mesh):
    cell = mesh.cells[0]
    mesh._findNeighboursOf(cell)
    assert len(cell.neighbours) > 0
    assert isinstance(cell.neighbours[0], Cell)
    assert cell in cell.neighbours[0].neighbours
