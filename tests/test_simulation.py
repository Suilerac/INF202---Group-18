from Simulation.simulation import Simulation
import pytest


@pytest.fixture
def standardSim():
    """
    Gives a simulation object running the standard time dependant
    simulation.
    """
    sim = Simulation("configs/test.toml")
    sim._initialCellOil()
    sim._solver._fieldIsTimeDependent = True
    return sim


@pytest.fixture
def faucetSim():
    """
    Gives a simulation object running the optimized simulation that relies
    on a constant vector field (the one provided in the task)
    """
    sim = Simulation("configs/test.toml")
    sim._initialCellOil()
    sim._solver._fieldIsTimeDependent = False
    return sim


def test_oilCount(faucetSim):
    """
    Tests that that oil gets added
    """
    assert 0 <= faucetSim.countAllOil()


def test_constantOilFaucet(faucetSim):
    """
    Tests that oil value stays constant in the faucet optimized sim
    """
    initialOil = faucetSim.countAllOil()
    faucetSim.run()
    finalOil = faucetSim.countAllOil()

    assert initialOil == pytest.approx(finalOil)


def test_constantOilStandard(standardSim):
    """
    Tests that oil value stays constant in the standard sim
    """
    initialOil = standardSim.countAllOil()
    standardSim.run()
    finalOil = standardSim.countAllOil()

    assert initialOil == pytest.approx(finalOil)


def test_compareResults(faucetSim, standardSim):
    """
    Tests that the faucetSim and standardSim gets the same results
    """
    # run both simulations
    faucetSim.run()
    standardSim.run()

    # compare the final result in each cell
    zipped = zip(faucetSim._mesh.cells, standardSim._mesh.cells)
    for cellFaucet, cellStandard in zipped:
        # oil densities should be the same
        assert cellFaucet.oilDensity == pytest.approx(cellStandard.oilDensity)
