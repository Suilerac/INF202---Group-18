from Simulation.simulation import Simulation


def main():
    sim = Simulation("")
    sim.run(endTime=0.5, numSteps=500, writeFrequency=20)
    print(f'Oil {"will" if sim.oilHitsFish else "wont"} hit the fish.')
    print(f"Total start value: {sim.totalOilStart}")
    print(f"Total end value: {sim.totalOilEnd}")


if __name__ == "__main__":
    main()
