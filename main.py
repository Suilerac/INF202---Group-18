import numpy as np
from Simulation.line import Line


def main():
    Line1 = [np.array([0.1, -1, 0]), np.array([1.5, -1.2, 0])]
    line = Line(Line1)
    print(line)


if __name__ == "__main__":
    main()
