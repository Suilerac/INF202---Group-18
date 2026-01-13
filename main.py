from Simulation.simulation import Simulation


def main():
    sim = Simulation("")
    sim.run(endTime=0.5, numSteps=500, writeFrequency=20)


if __name__ == "__main__":
    main()
