import numpy as np
import pytest
from Geometry.line import Line

# Testline
Line1 = [np.array([0, 0, 0]), np.array([1, 1, 0])]
Line2 = [np.array([0, 0, 0]), np.array([-2, 2, 0])]
Line3 = [np.array([.1, -1, 0]), np.array([3, -3, 0])]


@pytest.fixture
def line1():
    return Line(Line1)


@pytest.fixture
def line2():
    return Line(Line2)


@pytest.fixture
def line3():
    return Line(Line3)


def coordinates_test(line1, line2, line3):
    assert Line1 == line1.coordinates
    assert Line2 == line2.coordinates
    assert Line3 == line3.coordinates


def test_oil_value(line1, line2, line3):
    assert line1.oilValue == 0
    assert line2.oilValue == 0
    assert line3.oilValue == 0


def test_area_value(line1, line2, line3):
    assert line1.area == 0
    assert line2.area == 0
    assert line3.area == 0


def test_area_calculation(line1, line2, line3):
    assert line1._calculateArea() == 0
    assert line2._calculateArea() == 0
    assert line3._calculateArea() == 0


def test_flow_value(line1, line2, line3):
    assert line1.flow == [0, 0]
    assert line2.flow == [0, 0]
    assert line3.flow == [0, 0]


def test_string_conversion(line1, line2, line3):
    assert str(line1) == "[[0, 0, 0], [1, 1, 0]]"
    assert str(line2) == "[[0, 0, 0], [-2, 2, 0]]"
    assert str(line3) == "[[0.1, -1.0, 0.0], [3, -3, 0]]"


def test_oil_setter(line1):
    line1.oilValue = 4
    assert line1.oilValue == 4
