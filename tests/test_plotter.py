from Simulation.plotter import Plotter
from Geometry.mesh import Mesh
import pytest
import os


@pytest.fixture
def plotter():
    return Plotter(Mesh("meshes/simple_mesh.msh"))


def test_plotting(plotter):
    plotter.plot_current_values()


def test_save(plotter):
    plotter.save_current_plot("test.png")
    assert os.path.isfile("img/test.png")
    os.remove("img/test.png")
