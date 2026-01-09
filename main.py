from Geometry.mesh import Mesh
from Simulation.plotter import Plotter
import numpy as np
import os


def main():
    msh = Mesh("meshes/bay.msh")
    xstar = np.array([0.35, 0.45])
    for cell in msh.cells:
        cellCenter = np.array(cell.centerPoint[:2])
        finalVector = cellCenter - xstar
        finalNorm = np.linalg.norm(finalVector)
        oil = np.exp(-abs(finalNorm)**2/0.01)
        cell.oilValue = oil
    plotter = Plotter(msh)
    plotter.plot_current_values()
    plotter.save_current_plot("img.png")
    os.remove("img.png")


if __name__ == "__main__":
    main()
