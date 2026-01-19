from Simulation.plotter import Plotter
from Geometry.mesh import Mesh
import pytest
import os


@pytest.fixture
def plotter(tmp_path):
    image_dir = f"{tmp_path}/img"
    video_dir = f"{tmp_path}/vids"
    list_dir = f"{tmp_path}/list"
    return Plotter(Mesh("meshes/simple_mesh.msh"),
                   image_dir, video_dir, list_dir)


def test_ensure_image_dir(plotter):
    """
    Test that image directory gets created
    """
    assert os.path.isdir(plotter.image_dir)


def test_ensure_video_dir(plotter):
    """
    Test that video directory gets created
    """
    assert os.path.isdir(plotter.video_dir)


def test_ensure_list_dir(plotter):
    """
    Tests that list directory gets created
    """
    assert os.path.isdir(plotter.list_dir)


def test_image_txt_write(plotter):
    """
    Test that the plotter writes correctly to images.txt
    """
    plotter._write_temp_images()
    assert os.path.isfile(f"{plotter.list_dir}/images.txt")


def test_image_txt_content(plotter):
    """
    Tests that the correct items get written to images.txt
    """
    # Generate a test file so a file directory gets written
    # to images.txt
    testfile = open(f"{plotter.image_dir}/test.png", 'w')
    testfile.close()
    plotter._write_temp_images()
    # Check that the directory that gets written to images.txt is
    # the correct one
    with open(f"{plotter.list_dir}/images.txt", 'r', encoding='utf-8') as f:
        image = f.readline().strip().split(' ')[1].strip("'")
        assert os.path.isfile(image)


def test_save(plotter):
    """
    Tests that an image gets created by the plotter
    """
    plotter.save_current_plot(fileName="test.png")
    assert os.path.isfile(f"{plotter._image_dir}/test.png")


def test_video(plotter):
    """
    Tests that a video gets created by video_maker
    """
    plotter.plot_current_values()
    plotter.save_current_plot("test.png")
    plotter.video_maker()
    assert os.path.isfile(f"{plotter.video_dir}/simulation.mp4")


def test_cleanup(plotter):
    """
    Tests that cleanup correctly deletes appropriate files
    """
    plotter.plot_current_values()
    plotter.save_current_plot("test.png")
    plotter.video_maker()
    plotter.clean_up()
    assert not os.path.isfile(f"{plotter.image_dir}/test.png")
