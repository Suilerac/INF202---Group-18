from Simulation.solver import Solver
import numpy as np
import pytest


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


@pytest.mark.parametrize("coord, expectedVector", [
    (P1, np.array([.4, -.5])),
    (P2, np.array([.38, -.35])),
    (P3, np.array([.16, -.2])),
])
def test_vector_field(solver, coord, expectedVector):
    result = solver.vectorField(coord)
    assert np.allclose(result, expectedVector)


def test_average_velocity():
    pass


def test_Flow_value():
    pass


def test_Flux():
    pass
