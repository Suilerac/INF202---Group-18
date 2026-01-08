import numpy as np
import pytest
from Simulation.line import Line

Line1 = [np.array([0, 0, 0]), np.array([1, 1, 0])]

@pytest.fixture
def line():
    return Line(Line1)

def coordinates_test():
    assert Line1==Line(Line1)

def test_oil_value():
    line = Line(Line1)
    assert line.OilValue == 0

def test_area_value():
    line = Line(Line1)
    assert line.Area == 0

def test_area_calculation():
    line = Line(Line1)
    assert line._calculateArea() == 0

def test_flow_value():
    line = Line(Line1)
    assert line.FlowValue == [0,0]