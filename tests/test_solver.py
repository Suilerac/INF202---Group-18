from Simulation.solver import Solver
import numpy as np
import pytest

S = Solver()

P1 = np.array([.5, .5])
P2 = np.array([.35, .45])
P3 = np.array([.2, .2])


@pytest.fixture
def solver():
    return Solver()


@pytest.mark.parametrize("coord, expected", [
    (P1, .08208499862389),
    (P2, 1),
    (P3, .000203468369010),
])
def test_inital_oilValue(solver, coord, expected):
    result = solver.initalOil(coord)
    assert (result) == pytest.approx(expected)


def test_vector_field():
    pass


def test_average_velocity():
    pass


def test_Flow_value():
    pass


def test_Flux():
    pass
