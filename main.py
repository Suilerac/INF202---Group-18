from Simulation.simulation import Simulation
import time
from multiprocessing import Process


def main():
    sims = [
        Simulation("configs/default.toml"),
        Simulation("configs/test1.toml"),
        Simulation("configs/test2.toml"),
        Simulation("configs/test3.toml"),
    ]
    threads = []
    for sim in sims:
        t = Process(target=sim.run)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    for sim in sims:
        break
        sim.saveVid()


def single_sim():
    sim = Simulation("configs/test.toml")
    sim._initialCellOil()
    oilStart = sim.countAllOil()
    sim._solver._fieldIsTimeDependent = True
    sim.run()
    oilEnd = sim.countAllOil()
    print(oilStart, oilEnd)


if __name__ == "__main__":
    start = time.time()
    single_sim()
    end = time.time()
    print(f"Simulation spent {end - start} seconds")
