from Simulation.simulation import Simulation
import pytest


@pytest.fixture
def simulation():
    sim = Simulation("configs/test.toml")
    sim._initialCellOil()
    return sim


def test_oilCount(simulation):
    assert 0 <= simulation.countAllOil()


def test_constantOil(simulation):
    initialOil = simulation.countAllOil()
    simulation.run()
    finalOil = simulation.countAllOil()

    assert initialOil == pytest.approx(finalOil)
