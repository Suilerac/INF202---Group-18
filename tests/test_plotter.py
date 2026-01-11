from Simulation.plotter import Plotter
from Geometry.mesh import Mesh
import pytest
import os


@pytest.fixture
def plotter(tmp_path):
    image_dir = f"{tmp_path}/img"
    video_dir = f"{tmp_path}/vids"
    list_dir = str(tmp_path)
    return Plotter(Mesh("meshes/simple_mesh.msh"),
                   image_dir, video_dir, list_dir)


def test_ensure_directories(plotter):
    assert os.path.isdir(plotter.image_dir)
    assert os.path.isdir(plotter.video_dir)
    assert os.path.isdir(plotter.list_dir)


def test_plotting(plotter):
    plotter.plot_current_values()


def test_save(plotter):
    plotter.save_current_plot(fileName="test.png")
    assert os.path.isfile(f"{plotter._image_dir}/test.png")


def test_video(plotter, tmp_path):
    plotter.plot_current_values()
    plotter.save_current_plot("test.png")
    plotter.video_maker()
    assert os.path.isfile(f"{plotter.video_dir}/simulation.mp4")


def test_cleanup(plotter, tmp_path):
    plotter.plot_current_values()
    plotter.save_current_plot("test.png")
    plotter.video_maker()
    plotter.clean_up()
    assert not os.path.isfile(f"{plotter.image_dir}/test.png")
