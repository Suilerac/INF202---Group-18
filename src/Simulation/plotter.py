import matplotlib.pyplot as plt
import numpy as np


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
        plt.savefig(fileName)
        plt.close
