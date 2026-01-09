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


def test_video(plotter):
    plotter.plot_current_values()
    plotter.save_current_plot("test.png")
    plotter.video_maker()
    assert os.path.isfile("vids/simulation.mp4")
    os.remove("img/test.png")
    os.remove("vids/simulation.mp4")


def test_cleanup(plotter):
    plotter.plot_current_values()
    plotter.save_current_plot("test.png")
    plotter.video_maker()
    plotter.clean_up("images.txt")
    assert not os.path.isfile("img/test.png")
