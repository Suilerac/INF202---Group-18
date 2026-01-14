from Geometry.mesh import Mesh
from Geometry.line import Line
from Geometry.cells import Cell
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
        self._oilHitsFish = False
        self._fishing_grounds = [[0, 0.45], [0, 0.2]]
        self._faucets = []

    def run(self, endTime, writeFrequency, numSteps):
        self._initiateAllValues()
        createVideo = (0 < writeFrequency)

        if not createVideo:
            writeFrequency = 1

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
            if (elapsed % writeFrequency == 0 and createVideo):
                self._plot.plot_current_values()
                self._savePicture()
            elapsed += 1
            pbar.update(1)
        # after simulation is over, log the final result

        if createVideo:
            pbar.close()
            self._plot.video_maker("simulation.mp4", frameduration)
            self._plot.clean_up()

    def _step(self, dt):
        for sourceCell, targetCell, flowCoefficient in self._faucets:
            # If the source is empty there will be no flow to neighbours
            if sourceCell.oilValue < 0:
                continue
            # calculate the flow from A to B
            flow = sourceCell.oilValue * flowCoefficient * dt

            # Add the flow to the update
            sourceCell.update = sourceCell.update - flow
            targetCell.update = targetCell.update + flow

        for cell in self._mesh.cells:
            # Update the Oilvalues and reset the update for every cell
            cell.updateOilValue()
            # Check if there is any oil in the fishing area
            self._oilHitsFish = cell.inFishingGround and cell.oilValue > 0

    def _initiateAllValues(self):
        print("Updating initial oil values")
        self._initialCellValues()
        print("Checking if any cell is in the fishing area")
        self._updateCellFishBools()
        self._addAllNeighbours()
        print("Calculate flowvalue for each neighbour pair")
        self._initialFlowValues()
        self._createFaucets()

    def _createFaucets(self):
        """
        Creates an array of tuples called faucets.
        A faucet is a structure that describes the from one cell to another.
        In this task the vector field does not change with respect to time
        and the vertecies in the mesh will never their position.
        We can therfore calculate a constant coefficient of flow between any
        cell neighbour pair. The simulation will then turn into a simple lookup
        of COF's, cell source, and cell target.
        """
        self._faucets = []
        for sourceCell in self._mesh.cells:
            # We only consider oil flowing out from a main cell
            # and into its neigbours

            # there should not be any flow related to a line cell
            if isinstance(sourceCell, Line):
                continue

            # calculate the flow into each neighbour cell
            for targetCell, (_, flowValue) in sourceCell.neighbours.items():
                # We only consider the flow from the main cell
                # to the neighbour. Not the oil absorbed
                if (flowValue <= 0):
                    continue  # Line Cells has flowValue = 0 by default

                # Calculate flow out of the cell
                flowCoefficient = flowValue / sourceCell.area
                faucet = (sourceCell, targetCell, flowCoefficient)
                self._faucets.append(faucet)

    def _cellInFishingGrounds(self, cell: Cell) -> bool:
        center2d = cell.centerPoint[:2]
        x_range = self._fishing_grounds[0]
        y_range = self._fishing_grounds[1]
        return (
            (x_range[0] <= center2d[0] <= x_range[1]) and
            (y_range[0] <= center2d[1] <= y_range[1])
            )

    def _initialCellValues(self):
        for cell in self._mesh.cells:
            cell.oilValue = self._solver.initalOil(cell.centerPoint[:-1])
            cell.flow = self._solver.vectorField(cell.centerPoint[:-1])

    def _addAllNeighbours(self):
        exclude = 1
        for cell in tqdm(self._mesh.cells, desc="Finding neighbours"):
            self._mesh.findNeighboursOf(cell, exclude)
            exclude += 1

    def _updateCellFishBools(self):
        for cell in self._mesh.cells:
            cell.inFishingGround = self._cellInFishingGrounds(cell)

    def _initialFlowValues(self):
        for cell in self._mesh.cells:
            # nesting hell under this if statement.
            if isinstance(cell, Line):
                continue

            # code for activating a cell
            # simply adds the neighboors and the related flow value
            for ngh, (sharedCoords, flowValue) in cell.neighbours.items():
                if flowValue is not None:
                    continue

                # calulate flow value
                flowValue = self._solver.calculateFlowValue(
                    cell,
                    ngh,
                    sharedCoords
                )

                # add the flowValue to the neighbour pair
                cell.updateFlowToNeighbour(ngh, flowValue)
                ngh.updateFlowToNeighbour(cell, -flowValue)

    def countAllOil(self):
        """
        Returns a value for the total amount of oil in all cells
        """
        totalOil = 0
        for cell in self._mesh.cells:
            totalOil += cell.oilValue
        return totalOil

    def _savePicture(self):
        # Because the picture list is sorted alphabetically, it
        # is important to have a naming scheme where alphabetical sorting
        # and date sorting is identical
        plot_name = f"plot{self._plotNumber:0{self._plotDigits}d}.png"
        self._plot.save_current_plot(plot_name)
        self._plotNumber += 1

    @property
    def oilHitsFish(self):
        return self._oilHitsFish
