import pytest
from Simulation.mesh import Mesh


@pytest.fixture
def mesh():
    return Mesh("simple_mesh.msh")


# Assert that the lists of datapoints aren't left empty
def test_list_filling(mesh):
    assert len(mesh.cells) > 0
    assert len(mesh.points) > 0


# Assert that correct indexes are found
def test_index_search(mesh):
    assert mesh._findTriangleIndexes() == [8]
    assert mesh._findLineIndexes() == [4, 5, 6, 7]
