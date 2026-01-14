from Geometry.mesh import Mesh
from Geometry.line import Line
from Geometry.cells import Cell
from Simulation.solver import Solver
from Simulation.plotter import Plotter
from tqdm import tqdm
import toml
import math


class Simulation:
    def __init__(self, configFile):
        # Desired folder for video output (optional)
        self._outPutPath = "file path"
        self._plotNumber = 1
        self._plotDigits = 0
        self._oilHitsFish = False
        self._totalOilStart = 0
        self._totalOilEnd = 0

        # Config values
        self._configFile = configFile
        self._nSteps = 0
        self._tEnd = 0
        self._meshName = ""
        self._borders = []
        self._logName = ""
        self._writeFrequency = 0
        self._readConfig()

        # Object creations
        self._mesh = Mesh(self._meshName)
        self._simName = configFile.split('.')[0].split('/')[1]
        self._imagePath = f"temp/{self._simName}/img"
        self._listPath = f"temp/{self._simName}"
        self._plot = Plotter(
            self._mesh,
            image_dir=self._imagePath,
            list_dir=self._listPath,
            x_range=self._mesh.x_range,
            y_range=self._mesh.y_range)
        self._solver = Solver()

    def run(self):
        self._initiateAllValues()
        dt = self._tEnd / self._nSteps
        pbar = tqdm(total=self._nSteps, desc="Computing simulation")
        elapsed = 0
        while elapsed < self._nSteps:
            self._step(dt)
            if self._writeFrequency:
                # Must be nested due to modulo by 0 error
                if (elapsed % self._writeFrequency == 0):
                    frameAmount = self._nSteps / self._writeFrequency
                    # This is needed for proper sorting
                    # It is the amount of digits the suffix of each plot name
                    # needs for proper sorting
                    # Logic pulled from this stackoverflow post
                    # https://stackoverflow.com/questions/2189800/how-to-find-length-of-digits-in-an-integer
                    self._plotDigits = int(math.log10(frameAmount))+1
                    self._plot.plot_current_values()
                    self._savePicture()
            elapsed += 1
            pbar.update(1)
        # after simulation is over, log the final result
        pbar.close()

        for cell in self._mesh.cells:
            self._totalOilEnd += cell.oilValue

    def saveVid(self):
        if not self._writeFrequency:
            return
        frameAmount = self._nSteps / self._writeFrequency
        constvideotime = 5
        frameduration = constvideotime / frameAmount
        if self._writeFrequency:
            self._plot.video_maker(f"{self._simName}.mp4", frameduration)
            self._plot.clean_up()

    def _step(self, dt):
        for cell in self._mesh.cells:
            # In this loop we only consider oil flowing out from a main cell
            # and into its neigbours

            # There is no oil that can flow out of an empty cell
            # there should not be any flow related to a line cell
            if isinstance(cell, Line) or cell.oilValue < 0:
                continue

            # calculate the flow into each neighbour
            for neighbour, (_, flowValue) in cell.neighbours.items():
                # We only consider the flow from the main cell
                # to the neighbour. Not the oil absorbed
                if (flowValue <= 0):
                    continue  # Line Cells has flowValue = 0 by default

                # calculate the flux
                flux = self._solver.flux(
                    cell.oilValue,
                    neighbour.oilValue,
                    flowValue
                )
                # Calculate flow out of the cell
                flow = dt / cell.area * flux

                # Add the flow to the update
                cell.update = cell.update - flow
                neighbour.update = neighbour.update + flow

        for cell in self._mesh.cells:
            # Update the Oilvalues and reset the update for every cell
            cell.updateOilValue()
            # Check if there is any oil in the fishing area
            self._oilHitsFish = cell.inFishingGround and cell.oilValue > 0

    def _initiateAllValues(self):
        print("Updating initial oil values")
        self._initialCellValues()
        for cell in self._mesh.cells:
            self._totalOilStart += cell.oilValue

        self._updateCellFishBools()
        self._mesh.addAllNeighbours()
        print("Calculate flowvalue for each neighbour pair")
        self._initialFlowValues()

    def _savePicture(self):
        # Because the picture list is sorted alphabetically, it
        # is important to have a naming scheme where alphabetical sorting
        # and date sorting is identical
        plot_name = f"plot{self._plotNumber:0{self._plotDigits}d}.png"
        self._plot.save_current_plot(plot_name)
        self._plotNumber += 1

    def _cellInFishingGrounds(self, cell: Cell) -> bool:
        center2d = cell.centerPoint[:2]
        x_range = self._borders[0]
        y_range = self._borders[1]
        return (
            (x_range[0] <= center2d[0] <= x_range[1]) and
            (y_range[0] <= center2d[1] <= y_range[1])
            )

    def _initialCellValues(self):
        for cell in self._mesh.cells:
            cell.oilValue = self._solver.initalOil(cell.centerPoint[:-1])
            cell.flow = self._solver.vectorField(cell.centerPoint[:-1])

    def _addAllNeighbours(self):
        exclude = 0
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

    def _readConfig(self):
        with open(self._configFile, 'r') as file:
            config = toml.load(file)
        settings = config.get("settings", {})
        self._nSteps = settings.get("nSteps", 500)
        self._tEnd = settings.get("tEnd", 0.5)

        geometry = config.get("geometry", {})
        self._meshName = geometry.get("meshName", "meshes/bay.msh")
        self._borders = geometry.get("borders", [[0, 0.45], 0, 0.2])

        io = config.get("IO", {})
        self._logName = io.get("logName", "log")
        self._writeFrequency = io.get("writeFrequency", False)

    @property
    def oilHitsFish(self):
        return self._oilHitsFish

    @property
    def totalOilStart(self):
        return self._totalOilStart

    @property
    def totalOilEnd(self):
        return self._totalOilEnd
