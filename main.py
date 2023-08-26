from instance import Instance
from solver import Solver

if __name__ == '__main__':
    # TODO: aggiungere controlli che init e goal possano stare nella griglia
    istance = Instance(10,
                       10,
                       (0, 0),
                       (8, 7),
                       10,
                       5,
                       0.3,
                       0.5)
    grid = istance.grid
    grid.print()
    istance.plot()

    resolver = Solver(istance, 5)
    a, b, c = resolver.solve()
    print(a)



