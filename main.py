from Simulation.simulation import Simulation


def main():
    sim = Simulation("")
    sim.run(endTime=0.5, numSteps=500, writeFrequency=20)
    print(f"Oil {"will" if sim.oilHitsFish else "won't"} hit the fish.")


if __name__ == "__main__":
    main()
