from Geometry.mesh import Mesh
from Geometry.line import Line
from Geometry.cells import Cell
from Simulation.solver import Solver
from Simulation.plotter import Plotter
from InputOutput.tomlParser import TomlParser
from InputOutput.log import Log
import numpy as np
import math
from tqdm import tqdm


class Simulation:
    def __init__(self, configFile):
        """
        Simulates oil transport over a mesh as a results of applying
        a velocity field

        :param configFile: String describing path to config.toml file
        """
        # plot data for ordering images
        self._plotNumber = 1
        self._plotDigits = 0

        # Config values
        self._configFile = configFile
        self._toml = TomlParser(configFile)

        # Various variables
        self._simName = configFile.split('.')[0].split('/')[-1]
        self._imagePath = f"temp/{self._simName}/img"
        self._listPath = f"temp/{self._simName}"

        # Object creations
        self._log = Log(self._toml.logName, self._simName)
        self._logParameters()
        self._mesh = Mesh(self._toml.meshName)
        self._plot = Plotter(
            self._mesh,
            image_dir=self._imagePath,
            list_dir=self._listPath,
            video_dir=self._simName,
            x_range=self._mesh.x_range,
            y_range=self._mesh.y_range)
        self._solver = Solver()

        # List creations
        self._faucets = []
        self._fishingCells = self._initiateFishingCells()

    def run(self):
        """
        Run the simulation based on the parameters specified
        by the config.toml file. Creates a folder containing a
        video (optional), log and a picture of the final result
        """
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

        # Save final plot
        self._plot.plot_current_values
        self._plot.save_current_plot(self._simName, self._simName)

        if createVideo:
            self._plot.video_maker(f"{self._simName}.mp4", frameduration)
            self._plot.clean_up()

    def _runStandardSimulation(self, createVideo):
        """
        Runs a very general simulation where every flux calculation
        is done every time step. Will always give correct results.

        :param self: Boolean - createVideo
        """
        # initial values
        stepCount = 0
        dt = self._toml.tEnd / self._toml.nSteps

        # progressbar
        pbar = tqdm(
            total=self._toml.nSteps, desc=f"Computing sim {self._simName}"
            )
        while stepCount < self._toml.nSteps:
            # create image
            if (stepCount % self._toml.writeFrequency == 0 and createVideo):
                self._plot.plot_current_values()
                self._savePicture()

            # elapsed time
            t = dt * stepCount

            # simulation step
            self._standardStep(dt, t)
            stepCount += 1

            # log results
            fishOil = self._countOilInFishingGrounds()
            self._log.info(
                f"Oil density in fishing grounds at t={t:.2f}: {fishOil:.2f}"
                )

            # progress bar
            pbar.update(1)
        pbar.close()

        # create final image
        if (stepCount % self._toml.writeFrequency == 0 and createVideo):
            self._plot.plot_current_values()
            self._savePicture()

    def _standardStep(self, dt, t):
        """
        Handles a single timestep for the general simulation.

        :param dt: float - timestep
        :param t: float - elapsed time
        """
        # iterate over every cell
        for cell in self._mesh.cells:
            # line cell has no oil exchange
            if isinstance(cell, Line):
                continue
            # iterate over every neighbour
            for neighbour, scaledNormal in cell.neighbours.items():
                # line cell has no oil exchange
                if isinstance(neighbour, Line):
                    continue

                # Calulate average velocity between cell and ngh
                vA = self._solver.vectorField(cell.centerPoint, t)
                vB = self._solver.vectorField(neighbour.centerPoint, t)
                vAVG = self._solver._averageVelocity(vA, vB)

                # calulate flux between cell and ngh
                flux = self._solver.flux(
                    cell,
                    neighbour,
                    vAVG,
                    scaledNormal,
                )
                # apply flux
                cell.update -= dt * flux / cell.area

        # move oil from buffer variable to the actual oil density
        for cell in self._mesh.cells:
            cell.updateOilDensity()

    def _runFaucetOptimisedSimulation(self, createVideo):
        """
        Runs an optimized simulation based on assumptions of a
        constant velocityField over time. Precomputes every value in
        a structure called faucet and apply these every timestep.
        Reduces complex vector operations to simple multiplications

        :param self: Boolean - createVideo
        """
        # inital values
        stepCount = 0
        dt = self._toml.tEnd / self._toml.nSteps

        # cell velocity is constant and will be initialized once
        self._initialCellVelocity()
        self._createFaucets(dt)

        # progressbar
        pbar = tqdm(
            total=self._toml.nSteps, desc=f"Computing sim {self._simName}"
            )

        # simulation loop
        while stepCount < self._toml.nSteps:
            # create image
            if (stepCount % self._toml.writeFrequency == 0 and createVideo):
                self._plot.plot_current_values()
                self._savePicture()

            # take simulation step
            self._faucetStep()
            stepCount += 1

            # log results
            fishOil = self._countOilInFishingGrounds()
            t = dt * stepCount
            self._log.info(
                f"Oil density in fishing grounds at t={t:.2f}: {fishOil:.2f}"
                )
            # progress bar
            pbar.update(1)
        pbar.close()

        # create final image
        if (stepCount % self._toml.writeFrequency == 0 and createVideo):
            self._plot.plot_current_values()
            self._savePicture()

    def _faucetStep(self):
        # loop over every faucet
        for sourceCell, targetCell, flowAB, flowBA in self._faucets:
            # If the source has no oil there will be
            # no oil transport to its neighbours
            if sourceCell.oilDensity <= 0:
                continue

            # Update the update buffers with the faucet formula
            sourceCell.update -= sourceCell.oilDensity * flowAB
            targetCell.update += sourceCell.oilDensity * flowBA

        # move oil from buffer variable to the actual oil density
        for cell in self._mesh.cells:
            cell.updateOilDensity()

    def _createFaucets(self, dt):
        """
        Creates an array of tuples called faucets.
        A faucet is a structure that describes the from one cell to another.
        In this task the vector field does not change with respect to time
        and the vertecies in the mesh will never their position.
        We can therfore calculate a constant
        coefficient of velocity between any
        cell neighbour pair. The simulation will then turn into a simple lookup
        of COF's, cell source, and cell target.
        """
        # list for storing all faucets
        self._faucets = []
        for sourceCell in self._mesh.cells:
            # We only consider oil transport out of a main cell
            # and into its neigbours

            # there should not be any oil exchange related to a line cell
            if isinstance(sourceCell, Line):
                continue

            # calculate the velocity into each neighbour cell
            for targetCell, scaledNormal in sourceCell.neighbours.items():
                # there should not be any oil exchange related to a line cell
                if isinstance(targetCell, Line):
                    continue

                # We only consider the velocity from the main cell
                # to its neighbour. Not the oil the main cell wil absorb
                velocityAVG = self._solver._averageVelocity(
                    targetCell.velocity,
                    sourceCell.velocity,
                )
                # flowValue is a coefficient that measures how much the
                # avg velocity alignsw with the outgoing normal
                flowValue = np.dot(velocityAVG, scaledNormal)

                # if the alignment is less than 0 then this is oil absorbed
                # if the main cell = i, and ngh cell = j we can say that this
                # will be created as a differnet faucet from j -> i
                # in a upcoming iteration
                if (flowValue <= 0):
                    continue

                # Calculate the constant oil exchange coefficients
                flowAB = dt * flowValue / sourceCell.area
                flowBA = dt * flowValue / targetCell.area

                # create and store faucet
                faucet = (sourceCell, targetCell, flowAB, flowBA)
                self._faucets.append(faucet)

    def _inFishingGrounds(self, cell: Cell) -> bool:
        """
        Checks if a cells centerpoint is inside the domain of
        the fishing grounds

        :param cell: Cell object

        :rtype: bool
        """
        # fetch domain and centerpoint coord
        center2d = cell.centerPoint[:2]
        x_range = self._toml.borders[0]
        y_range = self._toml.borders[1]

        # simple domain check (also clever way to store result in cell)
        cell.inFishingGround = (
            (x_range[0] <= center2d[0] <= x_range[1]) and
            (y_range[0] <= center2d[1] <= y_range[1])
            )

        return cell.inFishingGround

    def _initialCellOil(self):
        """
        Initialize oildensities in every cell
        based on the presented function
        """
        for cell in self._mesh.cells:
            cell.oilDensity = self._solver.initalOil(cell.centerPoint[:-1])

    def _initialCellVelocity(self):
        """
        Initialize velocities in every cell
        based on the presented function
        """
        for cell in self._mesh.cells:
            cell.velocity = self._solver.vectorField(cell.centerPoint[:-1])

    def _initiateFishingCells(self):
        """
        check if the cells in the mesh lies withing
        the domain of the fishing grounds

        :rtype: list of cell objects
        """
        return [
            cell for cell in self._mesh.cells if self._inFishingGrounds(cell)
            ]

    def _countOilInFishingGrounds(self):
        return sum(cell.oilDensity for cell in self._fishingCells)

    def countAllOil(self):
        """
        Returns a scalar value for the total amount of oil in all cells
        """
        totalOil = 0
        for cell in self._mesh.cells:
            # convert oil density to amount
            totalOil += cell.oilDensity * cell.area
        return totalOil

    def _savePicture(self):
        """
        Saves a picture for the current mesh data
        """
        # Because the picture list is sorted alphabetically, it
        # is important to have a naming scheme where alphabetical sorting
        # and date sorting is identical
        plot_name = f"plot{self._plotNumber:0{self._plotDigits}d}.png"
        self._plot.save_current_plot(plot_name)
        self._plotNumber += 1

    def _logParameters(self):
        """
        logs the config file parameters
        """
        self._log.info(f"nSteps: {self._toml.nSteps}")
        self._log.info(f"tEnd: {self._toml.tEnd}")
        self._log.info(f"meshName: {self._toml.meshName}")
        self._log.info(f"borders: {self._toml.borders}")
        self._log.info(f"logName: {self._toml.logName}")
        self._log.info(f"writeFrequency: {self._toml.writeFrequency}")
