import numpy as np
import pytest
from Geometry.line import Line

# Testline
Line1 = [np.array([0, 0, 0]), np.array([1, 1, 0])]
Line2 = [np.array([0, 0, 0]), np.array([-2, 2, 0])]
Line3 = [np.array([.1, -1, 0]), np.array([3, -3, 0])]


@pytest.fixture
def line1():
    return Line(Line1, [])


@pytest.fixture
def line2():
    return Line(Line2, [])


@pytest.fixture
def line3():
    return Line(Line3, [])


@pytest.mark.parametrize("Line, expectedcoord", [
    (Line1, [np.array([0, 0, 0]), np.array([1, 1, 0])]),
])
def coordniates_test1(line1, Line, expectedcoord):
    """
    Tests that coordinates are set correctly for line1
    """
    result = line1.coordinates(Line)
    assert result == expectedcoord


@pytest.mark.parametrize("Line, expectedcoord", [
    (Line2, [np.array([0, 0, 0]), np.array([-2, 2, 0])]),
])
def coordniates_test2(line2, Line, expectedcoord):
    """
    Tests that coordinates are set correctly for line2
    """
    result = line2.coordinates(Line)
    assert result == expectedcoord


@pytest.mark.parametrize("Line, expectedcoord", [
    (Line3, [np.array([.1, -1, 0]), np.array([3, -3, 0])]),
])
def coordniates_test3(line3, Line, expectedcoord):
    """
    Tests that coordinates are set correctly for line3
    """
    result = line3.coordinates(Line)
    assert result == expectedcoord


@pytest.mark.parametrize("expectedOil", [
    (0),])
def test_oil_value1(line1, expectedOil):
    """
    Tests that oilvalue is set correctly for line1
    """
    result = line1.oilValue
    assert result == expectedOil


@pytest.mark.parametrize("expectedOil", [
    (0),])
def test_oil_value2(line2, expectedOil):
    """
    Tests that oilvalue is set correctly for line2
    """
    result = line2.oilValue
    assert result == expectedOil


@pytest.mark.parametrize("expectedOil", [
    (0),])
def test_oil_value3(line3, expectedOil):
    """
    Tests that oilvalue is set correctly for line3
    """
    result = line3.oilValue
    assert result == expectedOil


@pytest.mark.parametrize("expectedArea", [
    (0),])
def test_area_value1(line1, expectedArea):
    """
    Tests that area is set correctly for line1
    """
    result = line1.area
    assert result == expectedArea


@pytest.mark.parametrize("expectedArea", [
    (0),])
def test_area_value2(line2, expectedArea):
    """
    Tests that area is set correctly for line2
    """
    result = line2.oilValue
    assert result == expectedArea


@pytest.mark.parametrize("expectedArea", [
    (0),])
def test_area_value3(line3, expectedArea):
    """
    Tests that area is set correctly for line3
    """
    result = line3.oilValue
    assert result == expectedArea


@pytest.mark.parametrize("expectedArea", [
    (0),])
def test_area_calculation1(line1, expectedArea):
    """
    Tests that area gets calculated correctly for line1
    """
    result = line1._calculateArea()
    assert result == expectedArea


@pytest.mark.parametrize("expectedArea", [
    (0),])
def test_area_calculation2(line2, expectedArea):
    """
    Tests that area gets calculated correctly for line2
    """
    result = line2._calculateArea()
    assert result == expectedArea


@pytest.mark.parametrize("expectedArea", [
    (0),
])
def test_area_calculation3(line3, expectedArea):
    """
    Tests that area gets calculated correctly for line3
    """
    result = line3._calculateArea()
    assert result == expectedArea


@pytest.mark.parametrize("expectedFlow", [
    ([0, 0]),
])
def test_flow_value1(line1, expectedFlow):
    """
    Tests that flow is set correctly for line1
    """
    result = line1.flow
    assert result == expectedFlow


@pytest.mark.parametrize("expectedFlow", [
    ([0, 0]),
])
def test_flow_value2(line2, expectedFlow):
    """
    Tests that flow is set correctly for line2
    """
    result = line2.flow
    assert result == expectedFlow


@pytest.mark.parametrize("expectedFlow", [
    ([0, 0]),
])
def test_flow_value3(line3, expectedFlow):
    """
    Tests that flow is set correctly for line3
    """
    result = line3.flow
    assert result == expectedFlow


@pytest.mark.parametrize("expectedString", [
    ("[[0, 0, 0], [1, 1, 0]]"),
])
def test_string_conversion1(line1, expectedString):
    """
    Tests that string representation is set correctly for line1
    """
    result = str(line1)
    assert result == expectedString


@pytest.mark.parametrize("expectedString", [
    ("[[0, 0, 0], [-2, 2, 0]]"),
])
def test_string_conversion2(line2, expectedString):
    """
    Tests that string representation is set correctly for line2
    """
    result = str(line2)
    assert result == expectedString


@pytest.mark.parametrize("expectedString", [
    ("[[0.1, -1.0, 0.0], [3, -3, 0]]"),])
def test_string_conversion3(line3, expectedString):
    """
    Tests that string representation is set correctly for line3
    """
    result = str(line3)
    assert result == expectedString


@pytest.mark.parametrize("oilassert, expectedOilValue", [
    (4, 4),])
def test_oil_setter(line3, oilassert, expectedOilValue):
    """
    Tests that the oil setter works
    """
    line3.oilValue = oilassert
    assert line3.oilValue == expectedOilValue
