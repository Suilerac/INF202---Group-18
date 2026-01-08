from Simulation.mesh import Mesh

msh = Mesh("meshes/simple_mesh.msh")

# Assert that the lists of datapoints aren't left empty
assert len(msh.getCells()) > 0
assert len(msh.getPoints()) > 0

# Assert that correct indexes are found
assert msh._findTriangleIndexes() == [8]
assert msh._findLineIndexes() == [4, 5, 6, 7]
