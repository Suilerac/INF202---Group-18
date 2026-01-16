from Simulation.solver import Solver
from Geometry.triangle import Triangle
from Geometry.line import Line
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


# Create two trianlges that are neighbours and share point Pn1 and Pn2
S = Solver()

Pn1 = np.array([0, 1, 0])  # Neighbourpoint 1
Pn2 = np.array([1, 0, 0])  # Neighbourpoint 2
Pc1 = np.array([0, 0, 0])  # Corner 1
Pc2 = np.array([1, 1, 0])  # Corner 2

triangle1 = Triangle([Pn1, Pn2, Pc1], None)  # Triangle 1
triangle2 = Triangle([Pn1, Pn2, Pc2], None)  # Triangle 2
line1 = Line([Pc1, Pn1], None)           # Line)


Cells = [triangle1, triangle2, line1]
for cell in Cells:
    cell.oilValue = S.initalOil(cell.centerPoint[:2])
    cell.flow = S.vectorField(cell.centerPoint)


@pytest.mark.parametrize("CellA, CellB, expectedAvgVelocity", [
    (triangle1, triangle2, np.array([0.4, -0.5])),
    (triangle1, line1, np.array([0.383333, -0.1666667]))
])
def test_average_velocity_triangle(solver, CellA, CellB, expectedAvgVelocity):
    result = solver._averageVelocity(CellA.flow, CellB.flow)
    assert np.allclose(result, expectedAvgVelocity)


@pytest.mark.parametrize("CellA, CellB, SharedCoords, expectedFlow", [
    (triangle1, triangle2, [Pn1, Pn2], -.0999999999999999),
    (triangle1, line1, [Pc1, Pn1], 0),
])
def test_Flow_value_triangle(solver, CellA, CellB, SharedCoords, expectedFlow):
    result = solver.calculateFlowValue(CellA, CellB, SharedCoords)
    assert result == pytest.approx(expectedFlow)


@pytest.mark.parametrize("CellA, CellB, sharedCoords, expectedFlux", [
    (triangle1, triangle2, [Pn1, Pn2], -0.0249352208777296),
    (triangle1, line1, [Pc1, Pn1], 0),
])
def test_Flux(solver, CellA, CellB, sharedCoords, expectedFlux):
    CellA.flow = solver.vectorField(CellA.centerPoint)
    CellB.flow = solver.vectorField(CellB.centerPoint)
    avgVelocity = solver._averageVelocity(CellA.flow, CellB.flow)
    scaledNormal = CellA.calculateScaledNormal(sharedCoords)

    result = solver.flux(
        CellA,
        CellB,
        avgVelocity,
        scaledNormal
    )

    assert result == pytest.approx(expectedFlux)
