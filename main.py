from Simulation.simulation import Simulation


def main():
    sim = Simulation("")
    sim.run(endTime=0.5, numSteps=500, writeFrequency=20)
    willwont = "will" if sim.oilHitsFish else "won't"
    print(f"Oil {willwont} hit the fish.")
    print(f"Total start value: {sim.totalOilStart}")
    print(f"Total end value: {sim.totalOilEnd}")


if __name__ == "__main__":
    main()
