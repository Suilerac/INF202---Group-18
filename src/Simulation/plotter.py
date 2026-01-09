import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
import glob
import ffmpeg


class Plotter:
    def __init__(self, mesh):
        self._msh = mesh
        self._u = np.array([0, 1])
        self._sm = plt.cm.ScalarMappable(cmap='viridis')
        self._sm.set_array(self._u)
        self._cbar_ax = plt.gca().inset_axes([1, 0, 0.05, 1])
        plt.colorbar(self._sm, cax=self._cbar_ax, label='oilValue')

    def plot_current_values(self):
        """
        Generates a plot based on the current
        oil values of the cells in the mesh
        """
        for cell in self._msh.cells:
            # Make the points two dimensional
            coord = np.array([point[:2] for point in cell.coordinates])
            plt.gca().add_patch(
                plt.Polygon(
                    coord,
                    color=plt.cm.viridis(cell.oilValue),
                    alpha=0.9
                )
            )
        plt.xlabel('x-axis')
        plt.ylabel('y-axis')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.gca().set_aspect('equal')

    def save_current_plot(self, fileName):
        """
        Saves the currently generated plot as a file

        :param fileName: Description
        """
        imgDir = Path("img")
        imgDir.mkdir(parents=True, exist_ok=True)
        plt.savefig(imgDir / fileName)
        plt.close

    def video_maker(self, images, video_name='simulation.mp4'):
        folder = 'img'
        images = sorted(glob.glob(os.path.join(folder, "*.jpg")))  # natural/alphabetical sort
        list_path = images
        with open(list_path, "w", encoding="utf-8") as f:
            for img in images:
                safe = img.replace("\\", "/").replace("'", "'\\''")
                f.write(f"file '{safe}'\n")
                f.write("duration 1\n")     # Chooses duration of each frame in seconds
            # Optional: make last frame last the same duration
            # f.write("duration 0.04\n") == 1/25 seconds for 25 fps for example
        (
            ffmpeg
            .input(list_path, format='concat', safe=0)
            .output(video_name, vcodec='libx264', pix_fmt='yuv420p')
            .run())
        os.remove(list_path)        # Clean up the temporary file
        images = os.listdir("img")  # Get all images in img folder
        for img in images:
            os.remove(os.path.join("img", img))
