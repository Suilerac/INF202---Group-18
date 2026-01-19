from Simulation.simulation import Simulation
from InputOutput.commandlineParser import CommandlineParser
from tqdm import tqdm


def main():
    clp = CommandlineParser()
    clp.parse()
    clp.setConfigList()
    sims = [Simulation(config) for config in clp.configs]
    for sim in tqdm(sims, desc="Computing simulations:"):
        sim.run()


if __name__ == "__main__":
    main()
