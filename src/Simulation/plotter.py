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

    def save_current_plot(self, fileName, imgDir="img"):
        """
        Saves the currently generated plot as a file

        :param fileName: Description
        """
        imgDir = Path(imgDir)
        imgDir.mkdir(parents=True, exist_ok=True)
        plt.savefig(imgDir / fileName)
        plt.close

    def video_maker(self, video_name='simulation.mp4',
                    video_dir="vids", image_dir="img", list_dir=''):
        folder = image_dir
        # natural/alphabetical sort
        images = sorted(glob.glob(os.path.join(folder, "*.png")))
        list_path = f'{list_dir}/images.txt'
        output_loc = f"{video_dir}/{video_name}"
        with open(list_path, "w", encoding="utf-8") as f:
            for img in images:
                safe = img.replace("\\", "/").replace("'", "'\\''")
                f.write(f"file '{safe}'\n")
                # Chooses duration of each frame in seconds
                f.write("duration 1\n")
            # Optional: make last frame last the same duration
            # f.write("duration 0.04\n") == 1/25 seconds for 25 fps for example
        (
            ffmpeg
            .input(list_path, format='concat', safe=0)
            .output(output_loc, vcodec='libx264', pix_fmt='yuv420p')
            .run())

    def clean_up(self, list_path, imgage_dir="img"):
        os.remove(f"{list_path}/images.txt")  # Clean up the temporary file
        images = os.listdir(imgage_dir)  # Get all images in img folder
        for img in images:
            os.remove(os.path.join(imgage_dir, img))
