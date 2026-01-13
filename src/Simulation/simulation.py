from Geometry.mesh import Mesh
from Geometry.line import Line
from Simulation.solver import Solver
from Simulation.plotter import Plotter
from tqdm import tqdm
import math


class Simulation:
    def __init__(self, configFile):
        self._mesh = Mesh("meshes/bay.msh")
        self._plot = Plotter(self._mesh)
        self._solver = Solver()
        # Desired folder for video output (optional)
        self._outPutPath = "file path"
        self._plotNumber = 1
        self._plotDigits = 0

    def run(self, endTime, writeFrequency, numSteps):
        print("Updating initial oil values")
        self._initialCellValues()
        self._addAllNeighbours()
        print("Calculate flowvalue for each neighbour pair")
        self._initialFlowValues()

        frameAmount = numSteps / writeFrequency
        # This is needed for proper sorting
        # It is the amount of digits the suffix of each plot name will have
        # Logic pulled from this stackoverflow post
        # https://stackoverflow.com/questions/2189800/how-to-find-length-of-digits-in-an-integer
        self._plotDigits = int(math.log10(frameAmount))+1
        constvideotime = 5
        frameduration = constvideotime / frameAmount

        dt = endTime / numSteps

        pbar = tqdm(total=numSteps, desc="Computing simulation")

        elapsed = 0
        while elapsed < numSteps:
            self._step(dt)
            if (elapsed % writeFrequency == 0):
                self._plot.plot_current_values()
                self._savePicture()
            elapsed += 1
            pbar.update(1)
        # after simulation is over, log the final result
        pbar.close()
        self._plot.video_maker("simulation.mp4", frameduration)

    def _savePicture(self):
        # Because the picture list is sorted alphabetically, it
        # is important to have a naming scheme where alphabetical sorting
        # and date sorting is identical
        plot_name = f"plot{self._plotNumber:0{self._plotDigits}d}.png"
        self._plot.save_current_plot(plot_name)
        self._plotNumber += 1

    def _step(self, dt):
        for cell in self._mesh.cells:
            if isinstance(cell, Line):
                continue
            # calculate the incoming and outcoming flow for each neighbour
            totalFlux = 0
            for neighbour, values in cell.neighbours.items():
                flowValue = values[1]
                if (flowValue is None):
                    continue
                flux = self._solver.flux(cell, neighbour, flowValue)
                totalFlux += flux

            # update value calculatet from formula
            cell.update = - dt / cell.area * totalFlux

        for cell in self._mesh.cells:
            cell.updateOilValue()

    def _initialCellValues(self):
        for cell in self._mesh.cells:
            cell.oilValue = self._solver.initalOil(cell.centerPoint[:-1])
            cell.flow = self._solver.vectorField(cell.centerPoint[:-1])

    def _addAllNeighbours(self):
        for cell in tqdm(self._mesh.cells, desc="Finding neighbours"):
            self._mesh.findNeighboursOf(cell)

    def _initialFlowValues(self):
        for cell in self._mesh.cells:
            # nesting hell under this if statement.
            if isinstance(cell, Line):
                continue
            if (0 < cell.oilValue):
                # code for activating a cell
                # simply adds the neighboors and the related flow value
                for neighbour, values in cell.neighbours.items():
                    flowValue = values[1]
                    if flowValue is None:
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
