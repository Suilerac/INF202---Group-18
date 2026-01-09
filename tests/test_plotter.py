from Simulation.plotter import Plotter
from Geometry.mesh import Mesh
import pytest
import os


@pytest.fixture
def plotter():
    return Plotter(Mesh("meshes/simple_mesh.msh"))


def test_plotting(plotter):
    plotter.plot_current_values()


def test_save(plotter, tmp_path):
    temp = tmp_path / "img"
    temp.mkdir()
    plotter.save_current_plot(fileName="test.png", imgDir=str(temp))
    assert os.path.isfile(temp / "test.png")


def test_video(plotter, tmp_path):
    plotter.plot_current_values()
    imgDir = tmp_path / "img"
    plotter.save_current_plot("test.png", imgDir=str(imgDir))
    vidDir = tmp_path / "vids"
    vidDir.mkdir()
    plotter.video_maker(
        video_dir=str(vidDir), image_dir=str(imgDir), list_dir=tmp_path
        )
    assert os.path.isfile(vidDir / "simulation.mp4")


def test_cleanup(plotter, tmp_path):
    plotter.plot_current_values()
    vidDir = tmp_path / "vids"
    imgDir = tmp_path / "img"
    vidDir.mkdir()
    imgDir.mkdir()
    plotter.save_current_plot("test.png", str(imgDir))
    plotter.video_maker(
        video_dir=str(vidDir), image_dir=str(imgDir), list_dir=tmp_path
        )
    plotter.clean_up(str(tmp_path), imgage_dir=str(imgDir))
    assert not os.path.isfile(f"{str(imgDir)}/test.png")
