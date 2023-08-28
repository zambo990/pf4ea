import numpy as np
from path import Path
from grid import Grid


class Agents:
    def __init__(self, num_agents, grid: Grid, max_length: int):
        self.num_agents = num_agents
        self.grid = grid
        self.max_length = max_length

        self.starting_positions = []
        self.paths = []

        self.build_paths()

    def __build_path(self, grid: Grid) -> Path:
        path = Path([self.__get_new_random_start(grid)])
        if self.max_length == 0:
            length = 0
        else:
            length = np.random.randint(1, self.max_length + 1) #genero un cammino di lunghezza casuale ma < max_lenght
        while len(path) <= length:
            neighbors = grid.graph
            neighbors = neighbors[path[-1]][:]
            if len(neighbors) != 0:
                index = np.random.choice(range(len(neighbors)))
                next_neighbor = neighbors[index][0]
                # evito che gli agenti ripercorrano più volte le stesse celle
                while next_neighbor in path:
                    neighbors.pop(index)
                    if len(neighbors) == 0:
                        return path
                    index = np.random.choice(range(len(neighbors)))
                    next_neighbor = neighbors[index][0]
                path.append(next_neighbor)
        return path

    def __get_new_random_start(self, grid: Grid) -> (int, int):
        cell = grid.get_random_empty_cell()
        while cell in self.starting_positions:
            cell = grid.get_random_empty_cell()
        return cell

    def build_paths(self):
        for _ in range(self.num_agents):
            if self.__num_empty_cells() > 0:
                new_path = self.__build_path(self.grid)
                while not self.__is_collision_free(new_path, self.paths):
                    new_path = self.__build_path(self.grid)
                self.starting_positions.append(new_path[0])
                self.paths.append(new_path)
        return self.paths, self.starting_positions

    def __num_empty_cells(self):
        return len(self.grid.graph) - len(self.starting_positions)


    def __is_collision_free(self, new_path: Path, current_paths: [Path]):
        # prendo come orizzonti temporali da controllari gli istanti di tempo che vanno da 0 a max, dove max ricordiamo
        # che può assumere come valore massimo la lunghezza massima dei percorsi già esistenti + la lunghezza del nuovo percorso
        for t in range(max([len(p) for p in current_paths] + [len(new_path)])):
            for path in current_paths:
                # vincolo 1: all'istante t, la medesima cella non può essere occupata da 2 agenti distinti
                if path[t] == new_path[t]:
                    return False
                if t > 0:
                    # vincolo 2: due agenti che occupano celle adiacenti non possono scambiarsi il posto
                    if path[t] == new_path[t - 1] and new_path[t] == path[t - 1]:
                        return False

                    # vincolo 3: 2 agenti non possono incrociarsi durante il cambio cella
                    if new_path[t - 1][0] == path[t - 1][0] and new_path[t - 1][1] != path[t - 1][1]:
                        if new_path[t][0] == path[t][0] and new_path[t][1] != path[t][1]:
                            if new_path[t][1] == path[t - 1][1] and path[t][1] == new_path[t - 1][1]:
                                return False

                    if new_path[t - 1][1] == path[t - 1][1] and new_path[t - 1][0] != path[t - 1][0]:
                        if new_path[t][1] == path[t][1] and new_path[t][0] != path[t][0]:
                            if new_path[t][0] == path[t - 1][0] and path[t][0] == new_path[t - 1][0]:
                                return False
        return True




