from Simulation.simulation import Simulation


def main():
    sim = Simulation("")
    sim.run(endTime=0.5, numSteps=5000, writeFrequency=200)


if __name__ == "__main__":
    main()
