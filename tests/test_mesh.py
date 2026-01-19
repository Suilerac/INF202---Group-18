import pytest
import numpy as np
from Geometry.mesh import Mesh


@pytest.fixture
def mesh():
    return Mesh("meshes/simple_mesh.msh")


def test_list_filling(mesh):
    """
    Test that the list of pointIDs isn't left empty
    """
    assert len(mesh.points) > 0


def test_cell_list_filling(mesh):
    """
    Test that the list of cells isn't left empty
    """
    assert len(mesh.cells) > 0


# Assert that correct indexes are found
def test_index_search(mesh):
    """
    Test that the correct indexes are found
    """
    indexes = []
    for cell, index in mesh._findCellIndexes().items():
        indexes.append(index)
    assert indexes == [4, 5, 6, 7, 8]


def test_points(mesh):
    """
    Test that the cell coordinates are of the correct type
    """
    assert isinstance(mesh.cells[0].coordinates, np.ndarray)


def test_neighbours(mesh):
    """
    Test that neighbours are found, but not too many
    """
    mesh.addAllNeighbours()
    cell = mesh.cells[0]
    ngh = cell.neighbours
    assert 0 < len(ngh) < 3
