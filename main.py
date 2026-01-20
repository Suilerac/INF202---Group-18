from Simulation.simulation import Simulation
from InputOutput.commandlineParser import CommandlineParser


def main():
    clp = CommandlineParser()
    clp.parse()
    clp.setConfigList()
    sims = [Simulation(config) for config in clp.configs]
    for sim in sims:
        sim.run()


if __name__ == "__main__":
    main()
