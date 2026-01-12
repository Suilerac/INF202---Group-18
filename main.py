from Geometry.mesh import Mesh
from Simulation.plotter import Plotter
import numpy as np


def main():
    msh = Mesh("meshes/simple.msh")
    print(len(msh.cells))
    print(msh.cells[0].pointIDs)
    for cell in msh.cells:
        msh.findNeighboursOf(cell)


if __name__ == "__main__":
    main()
