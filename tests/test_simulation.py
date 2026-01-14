from Simulation.simulation import Simulation
import pytest


@pytest.fixture
def simulation():
    sim = Simulation("")
    sim._initiateAllValues()
    return sim


def test_oilCount(simulation):
    assert 0 <= simulation.countAllOil()


def test_constantOil(simulation):
    initialOil = simulation.countAllOil()
    simulation.run(0.5, 0, 20)
    finalOil = simulation.countAllOil()

    assert initialOil == pytest.approx(finalOil)
