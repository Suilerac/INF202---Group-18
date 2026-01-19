import pytest
import numpy as np
from Geometry.mesh import Mesh


@pytest.fixture
def mesh():
    return Mesh("meshes/simple_mesh.msh")


# Assert that the lists of datapoints aren't left empty
def test_list_filling(mesh):
    assert len(mesh.cells) > 0
    assert len(mesh.points) > 0


# Assert that correct indexes are found
def test_index_search(mesh):
    indexes = []
    for cell, index in mesh._findCellIndexes().items():
        indexes.append(index)
    assert indexes == [4, 5, 6, 7, 8]


def test_points(mesh):
    assert isinstance(mesh.cells[0].coordinates, np.ndarray)


def test_neighbours(mesh):
    mesh.addAllNeighbours()
    cell = mesh.cells[0]
    ngh = cell.neighbours
    assert len(ngh) > 0
    assert len(ngh) <= 3
