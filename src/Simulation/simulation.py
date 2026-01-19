from Geometry.mesh import Mesh
from Geometry.line import Line
from Geometry.cells import Cell
from Simulation.solver import Solver
from Simulation.plotter import Plotter
from InputOutput.tomlParser import TomlParser
from InputOutput.log import Log
import numpy as np
import math


class Simulation:
    def __init__(self, configFile):
        # Desired folder for video output (optional)
        self._outPutPath = "file path"
        self._plotNumber = 1
        self._plotDigits = 0

        # Config values
        self._configFile = configFile
        self._toml = TomlParser(configFile)
        self._log = Log(self._toml.logName)
        self._logParameters()

        # Object creations
        self._mesh = Mesh(self._toml.meshName)
        self._simName = configFile.split('.')[0].split('/')[-1]
        self._imagePath = f"temp/{self._simName}/img"
        self._listPath = f"temp/{self._simName}"
        self._plot = Plotter(
            self._mesh,
            image_dir=self._imagePath,
            list_dir=self._listPath,
            x_range=self._mesh.x_range,
            y_range=self._mesh.y_range)
        self._solver = Solver()

        # List creations
        self._faucets = []
        self._fishingCells = self._initiateFishingCells()

    def run(self):
        # Initial cell values
        self._initialCellOil()

        # find neighbour
        self._mesh.addAllNeighbours()

        # if Writefrequency is = 0, no video will be created
        createVideo = (0 < self._toml.writeFrequency)
        if not createVideo:
            # avoid div and divmod by 0
            self._toml.writeFrequency = 1

        # Constants for video creation
        constvideotime = 5
        frameAmount = self._toml.nSteps / self._toml.writeFrequency
        frameduration = constvideotime / frameAmount

        # This is needed for proper sorting
        # It is the amount of digits the suffix of each plot name will have
        # Logic pulled from this stackoverflow post
        # https://stackoverflow.com/questions/2189800/how-to-find-length-of-digits-in-an-integer
        self._plotDigits = int(math.log10(frameAmount))+1

        if (self._solver._fieldIsTimeDependent):
            # A time dependent vector field requires more
            # calculations per time step
            self._runStandardSimulation(createVideo)
        else:
            # if the vectorField is not related to time,
            # then we can use the faucet optimisation
            self._runFaucetOptimisedSimulation(createVideo)

        if createVideo:
            self._plot.video_maker(f"{self._simName}.mp4", frameduration)
            self._plot.clean_up()

    def _runStandardSimulation(self, createVideo):
        dt = self._toml.tEnd / self._toml.nSteps

        stepCount = 0
        while stepCount < self._toml.nSteps:
            t = dt * stepCount

            self._standardStep(dt, t)
            if (stepCount % self._toml.writeFrequency == 0 and createVideo):
                self._plot.plot_current_values()
                self._savePicture()

            stepCount += 1

            # after simulation is over, log the final result
            fishOil = self._countOilInFishingGrounds()
            self._log.info(
                f"Amount of oil in fishing grounds at t={t:.2f}: {fishOil:.2f}"
                )

    def _standardStep(self, dt, t):
        for cell in self._mesh.cells:
            if isinstance(cell, Line):
                continue
            for neighbour, scaledNormal in cell.neighbours.items():
                if isinstance(neighbour, Line):
                    continue

                vA = self._solver.vectorField(cell.centerPoint, t)
                vB = self._solver.vectorField(neighbour.centerPoint, t)
                vAVG = self._solver._averageVelocity(vA, vB)

                flux = self._solver.flux(
                    cell,
                    neighbour,
                    vAVG,
                    scaledNormal,
                )

                cell.update -= dt * flux / cell.area

        for cell in self._mesh.cells:
            cell.updateOilValue()

    def _runFaucetOptimisedSimulation(self, createVideo):
        dt = self._toml.tEnd / self._toml.nSteps
        self._initialCellFlow()
        self._createFaucets(dt)
        stepCount = 0

        while stepCount < self._toml.nSteps:
            self._faucetStep()

            if (stepCount % self._toml.writeFrequency == 0 and createVideo):
                self._plot.plot_current_values()
                self._savePicture()

            stepCount += 1
            # after simulation is over, log the final result
            fishOil = self._countOilInFishingGrounds()
            t = dt * stepCount
            self._log.info(
                f"Amount of oil in fishing grounds at t={t:.2f}: {fishOil:.2f}"
                )

    def _faucetStep(self):
        for sourceCell, targetCell, decrease, increase in self._faucets:
            # If the source is empty there will be no flow to neighbours
            if sourceCell.oilValue <= 0:
                continue

            # Add the flow to the update
            sourceCell.update -= sourceCell.oilValue * decrease
            targetCell.update += sourceCell.oilValue * increase

        for cell in self._mesh.cells:
            # Update the Oilvalues and reset the update for every cell
            cell.updateOilValue()

    def _createFaucets(self, dt):
        """
        Creates an array of tuples called faucets.
        A faucet is a structure that describes flow from one cell to another.
        In the given task the vector field does not change over time
        and the vertecies in the mesh have a fixed position.
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
            for targetCell, scaledNormal in sourceCell.neighbours.items():
                if isinstance(targetCell, Line):
                    continue
                # We only consider the flow from the main cell
                # to the neighbour. Not the oil absorbed
                velocityAVG = self._solver._averageVelocity(
                    targetCell.flow,
                    sourceCell.flow,
                )
                flowValue = np.dot(velocityAVG, scaledNormal)
                if (flowValue <= 0):
                    continue  # Line Cells has flowValue = 0 by default

                # Calculate flow out of the cell
                decrease = dt * flowValue / sourceCell.area
                increase = dt * flowValue / targetCell.area
                faucet = (sourceCell, targetCell, decrease, increase)
                self._faucets.append(faucet)

    def _inFishingGrounds(self, cell: Cell) -> bool:
        center2d = cell.centerPoint[:2]
        x_range = self._toml.borders[0]
        y_range = self._toml.borders[1]
        return (
            (x_range[0] <= center2d[0] <= x_range[1]) and
            (y_range[0] <= center2d[1] <= y_range[1])
            )

    def _initialCellOil(self):
        for cell in self._mesh.cells:
            cell.oilValue = self._solver.initalOil(cell.centerPoint[:-1])

    def _initialCellFlow(self):
        for cell in self._mesh.cells:
            cell.flow = self._solver.vectorField(cell.centerPoint[:-1])

    def _initiateFishingCells(self):
        return [
            cell for cell in self._mesh.cells if self._inFishingGrounds(cell)
            ]

    def _countOilInFishingGrounds(self):
        return sum(cell.oilValue for cell in self._fishingCells)

    def countAllOil(self):
        """
        Returns a value for the total amount of oil in all cells
        """
        totalOil = 0
        for cell in self._mesh.cells:
            totalOil += cell.oilValue * cell.area
        return totalOil

    def _savePicture(self):
        # Because the picture list is sorted alphabetically, it
        # is important to have a naming scheme where alphabetical sorting
        # and date sorting is identical
        plot_name = f"plot{self._plotNumber:0{self._plotDigits}d}.png"
        self._plot.save_current_plot(plot_name)
        self._plotNumber += 1

    def _logParameters(self):
        self._log.info(f"nSteps: {self._toml.nSteps}")
        self._log.info(f"tEnd: {self._toml.tEnd}")
        self._log.info(f"meshName: {self._toml.meshName}")
        self._log.info(f"borders: {self._toml.borders}")
        self._log.info(f"logName: {self._toml.logName}")
        self._log.info(f"writeFrequency: {self._toml.writeFrequency}")
