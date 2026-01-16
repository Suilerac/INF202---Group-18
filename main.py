from Simulation.simulation import Simulation
from InputOutput.commandlineParser import CommandlineParser
from multiprocessing import Process
from tqdm import tqdm


def main():
    clp = CommandlineParser()
    clp.parse()
    clp.setConfigList()
    sims = [Simulation(config) for config in clp.configs]
    threads = []
    if len(sims) > 1:  # If more than one, then we use multithreading
        for sim in sims:
            t = Process(target=sim.run)
            threads.append(t)
        for t in tqdm(threads, desc="Computing simulations"):
            t.start()
        for t in threads:
            t.join()
    else:
        sims[0].run()


if __name__ == "__main__":
    main()
