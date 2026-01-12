from Simulation.simulation import Simulation


def main():
    sim = Simulation("")
    dt = 0.5/500
    sim.run(endTime=0.5, nSteps=500, writeFrequency=20, dt=dt)


if __name__ == "__main__":
    main()
