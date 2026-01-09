import numpy as np
from Geometry.line import Line
from Geometry.mesh import Mesh


def main():
    msh = Mesh("meshes/simple_mesh.msh")
    print(msh.cells[0].coordinates)


if __name__ == "__main__":
    main()
