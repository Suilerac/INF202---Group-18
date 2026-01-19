from Simulation.simulation import Simulation
import pytest


@pytest.fixture
def standardSim():
    sim = Simulation("configs/test.toml")
    sim._initialCellOil()
    sim._solver._fieldIsTimeDependent = True
    return sim


@pytest.fixture
def faucetSim():
    sim = Simulation("configs/test.toml")
    sim._initialCellOil()
    sim._solver._fieldIsTimeDependent = False
    return sim


def test_oilCount(faucetSim):
    assert 0 <= faucetSim.countAllOil()


def test_constantOil(faucetSim, standardSim):
    initialOil = faucetSim.countAllOil()
    faucetSim.run()
    finalOil = faucetSim.countAllOil()

    assert initialOil == pytest.approx(finalOil)

    initialOil = standardSim.countAllOil()
    standardSim.run()
    finalOil = standardSim.countAllOil()

    assert initialOil == pytest.approx(finalOil)


def test_compareResults(faucetSim, standardSim):
    # run both simulations
    faucetSim.run()
    standardSim.run()

    # compare the final result in each cell
    zipped = zip(faucetSim._mesh.cells, standardSim._mesh.cells)
    for cellFaucet, cellStandard in zipped:
        # oilvalues should be the same
        assert cellFaucet.oilValue == pytest.approx(cellStandard.oilValue)
