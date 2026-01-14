from Simulation.simulation import Simulation
import time
from multiprocessing import Process


def main():
    sims = [Simulation("configs/default.toml"),
            Simulation("configs/test1.toml"),
            Simulation("configs/test2.toml")]
    threads = []
    for sim in sims:
        t = Process(target=sim.run)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    for sim in sims:
        sim.saveVid()


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Simulation spent {end - start} seconds")
