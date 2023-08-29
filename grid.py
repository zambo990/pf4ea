import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer

class Grid:

    # scelta progettuale: trattandosi di grafi potenzialmente grandi, per risparmiare memoria, si sceglie di usare
    # come modalità di rappresentazione le liste di adiacenza, ciò ha però lo svantaggio di aumentare i tempi di
    # ricerca dei vertici adiacenti ad un vertice dato

    def __init__(self, width: int, height: int, obstacle_percentage=0.1, conglomeration_ratio=0.4):
        start = timer()

        self.grid = np.zeros((height, width))
        self.empty_cells = []
        for i in range(height):
            for j in range(width):
                self.empty_cells += [(i, j)]
        self.height = height - 1
        self.width = width - 1
        self.obstacle_ratio = obstacle_percentage
        self.conglomeration_ratio = conglomeration_ratio

        self.num_cells = width * height
        self.num_obstacles = int(self.num_cells * obstacle_percentage)

        # aggiungo gli ostacoli alla griglia
        self.__add_obstacles()

        #salvo la lista di adiacenza all'interno di una variabile, in modo tale da doverla generare solo 1 volta
        self.graph = self.get_G()

        end = timer()
        self.execution_time = end - start

    
    def __add_obstacles(self):
        obstacles = self.num_obstacles
        while obstacles > 0:
            (x, y) = self.get_random_empty_cell()
            self.grid[(x, y)] = 1
            self.empty_cells.remove((x,y))
            obstacles -= 1
            obstacles = self.__add_conglomerated_obstacles((x,y), obstacles)

    def get_random_empty_cell(self):
        index = np.random.randint(0, len(self.empty_cells))
        return self.empty_cells[index]


    def __add_conglomerated_obstacles(self, actual_cell, obstacles: int):
        adjacent_cells = self.get_empty_adiacent_cells(actual_cell)
        while (obstacles > 0 and self.__conglomeration_probability() and
               len(adjacent_cells) > 0):
            adjacent_cells = list(set(adjacent_cells)) #elimino elementi duplicati
            index = np.random.randint(0, len(adjacent_cells))
            selected_adiacent = adjacent_cells.pop(index)
            self.grid[selected_adiacent] = 1
            self.empty_cells.remove(selected_adiacent)
            obstacles -= 1
            adjacent_cells += self.get_empty_adiacent_cells(selected_adiacent)
        return obstacles


    def get_adjacent_cells(self, actual_cell, diagonals = False):
        #NB ricorda che con le matrici Numpy le coordinate x ed y sono invertite rispetto alle coordinate della griglia

        cells = []
        if actual_cell[0] > 0: #prendo la cella a nord
            cells.append((actual_cell[0] - 1, actual_cell[1]))
        if actual_cell[0] < self.height: #prendo la cella a sud
            cells.append((actual_cell[0] + 1, actual_cell[1]))
        if actual_cell[1] > 0: #prendo la cella a ovest
            cells.append((actual_cell[0], actual_cell[1] - 1))
        if actual_cell[1] < self.width: #prendo la cella a est
            cells.append((actual_cell[0], actual_cell[1] + 1))

        #il parametro diagonals serve per definire se prendere anche le celle in diagonale, utile per
        #il ri-utilizzo di questo metodo in più punti del codice
        if diagonals:
            if actual_cell[0] > 0 and actual_cell[1] > 0: #prendo la cella a nord-ovest
                cells.append((actual_cell[0] - 1, actual_cell[1] - 1))
            if actual_cell[0] < self.height and actual_cell[1] > 0: #prendo la cella a sud-ovest
                cells.append((actual_cell[0] + 1, actual_cell[1] - 1))
            if actual_cell[0] > 0 and actual_cell[1] < self.width: #prendo la cella nord-est
                cells.append((actual_cell[0] - 1, actual_cell[1] + 1))
            if actual_cell[0] < self.height and actual_cell[1] < self.width: #prendo la cella a sud-est
                cells.append((actual_cell[0] + 1, actual_cell[1] + 1))
        return cells

    def get_empty_adiacent_cells(self, actual_cell, diagonals = False):
        cells = self.get_adjacent_cells(actual_cell, diagonals)
        empty_cells = []
        for el in cells:
            if el in self.empty_cells:
                empty_cells.append(el)
        return empty_cells

    def __conglomeration_probability(self):
        return (np.random.random_sample(1) < self.conglomeration_ratio)[0]

    def print(self): #usato solo per fare debugging
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i][j] == 0:
                    print('.', end='')
                else:
                    print('█', end='')
            print()

    def plot(self, show=True):
        plt.title(
            f'{self.grid.shape[1]} x {self.grid.shape[0]}\nObstacles: {self.num_obstacles} / {self.grid.size}')
        plt.pcolormesh(1 - self.grid, edgecolors='#777', linewidth=0.5, cmap='gray', vmin = 0, vmax = 1)
        plt.xticks(range(0, self.grid.shape[1], 1))
        plt.yticks(range(0, self.grid.shape[0], 1))
        ax = plt.gca()
        ax.invert_yaxis()
        ax.set_aspect('equal')
        for tick in ax.xaxis.get_majorticklabels():
            tick.set_horizontalalignment("left")
        for tick in ax.yaxis.get_majorticklabels():
            tick.set_verticalalignment("top")
        if show:
            plt.show(block=False)

    def get_G(self):
        adj = {}
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                # non creo liste di adiacenza per gli ostacoli
                if self.grid[i, j] == 0:
                    empty_neighbors = self.get_empty_adiacent_cells((i, j), True)
                    empty_neighbors = [(n, self.get_W((i, j), n)) for n in empty_neighbors]
                    adj[(i, j)] = empty_neighbors
        return adj

    def get_W(self, actual_cell, adjacent_cell):
        if actual_cell[0] == adjacent_cell[0] or actual_cell[1] == adjacent_cell[1]:
            return 1
        else:
            return np.sqrt(2)

    def get_path_cost(self, path):
        cost = 0
        for t in range(len(path) - 1):
            cost += self.get_W(path[t], path[t + 1])
        return cost

    def get_num_waits(self, path):
        count = 0
        for t in range(len(path) - 1):
            if path[t] == path[t + 1]:
                count += 1
        return count