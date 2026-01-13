from Simulation.solver import Solver
import numpy as np
import pytest


expectedValues = {
    "coord": np.array([0.5, 0.5, 0],  # Point 1
                      [0.2, 0.9, 0],  # Point 2
                      [0, 0, 0]),      # Point 3
    "oilValues": []
    }


@pytest.fixture
def solver():
    return Solver()


def test_inital_oilValue():
    # for i in range(3):
    # answer=expectedValues["oilValue"][i]
    pass


def test_vector_field():
    pass


def test_average_velocity():
    pass


def test_Flow_value():
    pass


def test_Flux():
    pass
