from Geometry.mesh import Mesh
from Geometry.line import Line
from Simulation.solver import Solver
from Simulation.plotter import Plotter
from tqdm import tqdm


class Simulation:
    def __init__(self, configFile):
        self._mesh = Mesh("meshes/bay.msh")
        self._plot = Plotter(self._mesh)
        self._solver = Solver()
        # Desired folder for video output (optional)
        self._outPutPath = "file path"

    def run(self, endTime, dt, writeFrequency, nSteps):
        print("Updating initial oil values")
        self._initialCellValues()
        print("Finding neighbours")
        self._addAllNeighbours()
        print("Neighbours found")
        elapsed = 0
        frameAmount = nSteps / writeFrequency
        constvideotime = 10
        frameduration = constvideotime / frameAmount
        plot_number = 0

        pbar = tqdm(total=nSteps, desc="Computing simulation")

        while elapsed < nSteps:
            self._step(dt)
            if (elapsed % writeFrequency == 0):
                plot_name = f"plot{plot_number}.png"
                self._plot.plot_current_values()
                self._plot.save_current_plot(plot_name)
                plot_number += 1
            elapsed += 1
            pbar.update(1)
        # after simulation is over, log the final result
        pbar.close()
        self._plot.video_maker("simulation.mp4", frameduration)

    def _step(self, dt):
        for cell in self._mesh.cells:
            # nesting hell under this if statement.
            if isinstance(cell, Line):
                continue
            if (0 < cell.oilValue):
                # code for activating a cell
                # simply adds the neighboors and the related flow value
                for neighbour, values in cell.neighbours.items():
                    # would be nice if the find neighboors method returned
                    # a tuple = (neigboor cell object, shared coords)
                    sharedCoords = values[0]
                    # sharedflow value
                    flowValue = self._solver.calculateFlowValue(
                        cell,
                        neighbour,
                        sharedCoords
                    )
                    cell.updateFlowToNeighbour(neighbour, flowValue)
                    neighbour.updateFlowToNeighbour(cell, -flowValue)

            totalFlux = 0
            for neighbour, values in cell.neighbours.items():
                flowValue = values[1]
                flux = self._solver.flux(cell, neighbour, flowValue)
                totalFlux += flux
            # update value calculatet from formula
            cell._update = dt / cell.area * totalFlux
        for cell in self._mesh.cells:
            cell.updateOilValue()

    def _initialCellValues(self):
        for cell in self._mesh.cells:
            cell.oilValue = self._solver.initalOil(cell.centerPoint[:-1])
            cell.flow = self._solver.vectorField(cell.centerPoint[:-1])

    def _addAllNeighbours(self):
        for cell in tqdm(self._mesh.cells, desc="Finding neighbours"):
            self._mesh.findNeighboursOf(cell)
