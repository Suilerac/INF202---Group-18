from src.Geometry.mesh import Mesh
from src.Simulation.solver import Solver
import numpy as np


class Simulation:
    def __init__(self, configFile):
        self.mesh = Mesh(configFile)
        # Desired folder for video output (optional)
        self.outPutPath = "file path"

    def run(self, endTime, dt, writeFrequency):
        elapsed = 0

        while elapsed < endTime:
            self._step(dt)
            if (elapsed % writeFrequency == 0):
                pass  # add plotter here

            elapsed += dt
        # after simulation is over, log the final result

    def _step(self, dt):
        for cell in self.mesh.cells:
            # nesting hell under this if statement.
            if (0 < cell.Oilvalue):
                # code for activating a cell
                # simply adds the neighboors and the related flow value
                neighboors = self.mesh.findNeighboursOf(cell)
                for neighboor in neighboors:
                    # would be nice if the find neighboors method returned
                    # a tuple = (neigboor cell object, shared coords)
                    sharedCoords = np.array[[0, 0, 0], [1, 1, 1]]
                    # sharedflow value
                    flowValue = Solver.calulateFlowValue(
                        cell,
                        neighboor,
                        sharedCoords
                    )
                # needs edgecase for lineCell. flowvalue should to 0.
                    cell.addNeighboor(neighboor, flowValue)

            totalFlux = 0
            for neighboor, flowValue in cell.neighbours.items():
                flux = Solver.flux(cell, neighboor, flowValue)
                totalFlux += flux
            # update value calculatet from formula
            cell._update = dt / cell.area * totalFlux

        for cell in self.mesh.cells:
            cell.updateOilValue()
