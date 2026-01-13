from Geometry.mesh import Mesh
from Geometry.line import Line
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
import numpy as np
from pathlib import Path
import os
import glob
import ffmpeg


class Plotter:
    def __init__(self, mesh: Mesh,
                 image_dir: str = 'temp/img',
                 video_dir: str = 'vids',
                 list_dir: str = 'temp'):
        """
        A class to handle matplotlib logic, and also handle
        file logic related to the matplotlib plots, such as
        image files and video files, and related temporary files.

        :param image_dir: A string describing the file path you want
            plot images saved in. Default is ./temp/img

        :param video_dir: A string describing the file path you want
            plot videos saved in. Default is ./vids

        :param list_dir: A string describing the file path you want
            the temporary images.txt saved in. Images.txt is a
            temporary file used by the video maker to compile a
            sorted list of all images that will make up the video.
            Default is ./temp
        """

        self._msh = mesh

        # File paths
        self._image_dir = image_dir
        self._video_dir = video_dir
        self._list_dir = list_dir
        self._ensure_paths()
        self._list_path = f"{list_dir}/images.txt"

        # Matplotlib initialization
        self._u = np.array([0, 1])
        self._sm = plt.cm.ScalarMappable(cmap='viridis')
        self._sm.set_array(self._u)
        self._cbar_ax = plt.gca().inset_axes([1, 0, 0.05, 1])
        plt.colorbar(self._sm, cax=self._cbar_ax, label='oilValue')

    @property
    def image_dir(self) -> str:
        return self._image_dir

    @property
    def video_dir(self) -> str:
        return self._video_dir

    @property
    def list_dir(self) -> str:
        return self._list_dir

    def plot_current_values(self):
        """
        Generates a plot based on the current
        oil values of the cells in the mesh
        """
        line_coords = []
        line_values = []
        poly_coords = []
        poly_values = []
        for cell in self._msh.cells:
            # Make the points two dimensional
            coord = np.array([point[:2] for point in cell.coordinates])
            if isinstance(cell, Line):
                line_coords.append(coord)
                line_values.append(cell.oilValue)
            else:
                poly_coords.append(coord)
                poly_values.append(cell.oilValue)
        polcol = PolyCollection(
            verts=poly_coords,
            array=poly_values,
            cmap='viridis',
            alpha=0.9
        )
        lincol = LineCollection(segments=line_coords, linewidths=line_values)
        plt.gca().add_collection(polcol)
        plt.gca().add_collection(lincol)
        plt.xlabel('x-axis')
        plt.ylabel('y-axis')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.gca().set_aspect('equal')

    def save_current_plot(self, fileName: str):
        """
        Saves the currently generated plot as a file

        :param fileName: Desired name of the image file.
            Must include file type.
            Example: "image.png"
        """
        plt.savefig(f"{self._image_dir}/{fileName}")
        plt.close

    def video_maker(self,
                    video_name: str = 'simulation.mp4',
                    frame_duration: float = 1):
        """_
        A function that loops through a txt file of image paths
        and makes a video file out of it.

        :param video_name: The wanted file name for the final product.
            Must include the file type. Example: "simulation.mp4"
        """
        self._write_temp_images(frame_duration)
        output_loc = f"{self._video_dir}/{video_name}"
        # Reads the arguments in image.txt through the input function
        # Writes the video file in the output function
        ffmpeg.input(
            self._list_path, format='concat', safe=0
            ).output(
                output_loc, vcodec='libx264', pix_fmt='yuv420p'
                ).run()

    def clean_up(self):
        """
        A function to clean up the temporary files made in the process
        of generating the video.
        """
        # Clean up the temporary images list
        os.remove(self._list_path)
        images = os.listdir(self._image_dir)  # Get all images in img folder
        for img in images:
            os.remove(os.path.join(self._image_dir, img))

    def _write_temp_images(self, frame_duration: float = 1):
        """
        A function to write the temporary images.txt file needed for
        video creation.

        :param frame_duration: The amount of seconds each frame should be on
            screen during the video. Example 60fps: 1/60 = 0.01666
        """
        images = sorted(glob.glob(os.path.join(self._image_dir, "*.png")))
        with open(self._list_path, 'w', encoding='utf-8') as txtfile:
            for img in images:
                abs_path = os.path.abspath(img)
                safe = abs_path.replace("\\", "/").replace("'", "'\\''")
                txtfile.write(f"file '{safe}'\n")
                txtfile.write(f"duration {frame_duration}\n")

    def _ensure_paths(self):
        """
        Upon object initialization, this method is run to ensure that
        the important directories for temporary files and the video
        actually exist, and creates them if they don't.
        """
        vid = Path(self._video_dir)
        img = Path(self._image_dir)
        ls = Path(self._list_dir)
        vid.mkdir(parents=True, exist_ok=True)
        img.mkdir(parents=True, exist_ok=True)
        ls.mkdir(parents=True, exist_ok=True)
