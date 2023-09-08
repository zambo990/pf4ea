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
        self.num_agents = len(self.paths) # aggiorno il numero di agenti, nel caso in cui non fosse stato possibile generare tutti gli agenti

    def __build_path(self) -> Path:
        path = Path([self.__get_new_random_start()])
        if self.max_length == 0:
            length = 0
        else:
            length = np.random.randint(0, self.max_length) #genero un cammino di lunghezza casuale ma <= max_lenght

        t = len(path) # rappresenta l'istante per cui devo selezionare la nuova cella nel percorso, in questo caso ottengo sempre 1
        while t <= length:
            neighbors = self.grid.graph #prendo la lista di adiacenza
            neighbors = neighbors[path[-1]][:] #prendo la lista di adiacenza per l'elemento all'istante t-1
            neighbors = [el [0] for el in neighbors] # elimino i costi

            for existing_path in self.paths:
                # vincolo 1: all'istante t, la medesima cella non può essere occupata da 2 agenti distinti
                if existing_path[t] in neighbors:
                    neighbors.remove(existing_path[t])

                # vincolo 2: due agenti che occupano celle adiacenti non possono scambiarsi il posto
                if existing_path[t] == path[t-1] and existing_path[t-1] in neighbors:
                    neighbors.remove(existing_path[t-1])

                # vincolo 3: 2 agenti non possono incrociarsi durante il cambio cella
                if path[t - 1][0] == existing_path[t - 1][0] and path[t - 1][1] != existing_path[t - 1][1]:
                    for cell in neighbors:
                        if cell[0] == existing_path[t][0] and cell[1] != existing_path[t][1]:
                            if cell[1] == existing_path[t - 1][1] and existing_path[t][1] == path[t - 1][1]:
                                neighbors.remove(cell)

                if path[t - 1][1] == existing_path[t - 1][1] and path[t - 1][0] != existing_path[t - 1][0]:
                    for cell in neighbors:
                        if cell[1] == existing_path[t][1] and cell[0] != existing_path[t][0]:
                            if cell[0] == existing_path[t - 1][0] and existing_path[t][0] == path[t - 1][0]:
                                neighbors.remove(cell)

            # elimino dalle celle adiacenti, tutte le celle già percorse, in modo da evitare backtracking
            for p in path:
                for el in neighbors:
                    if el == p:
                        neighbors.remove(el)

            if len(neighbors) != 0:
                index = np.random.choice(len(neighbors))
                next_neighbor = neighbors[index]
                path.append(next_neighbor)
                t += 1
            else:
                return path
        return path

    def __get_new_random_start(self) -> (int, int):
        empty_starts = list(self.grid.empty_cells.keys())
        for el in self.starting_positions: #evito di selezionare una cella di partenza già occupata da un altro agente
            if el in empty_starts:
                empty_starts.remove(el)
        if len(empty_starts) > 0:
            index = np.random.randint(0, len(empty_starts))
            cell = empty_starts[index]
            self.starting_positions.append(cell)
            return cell
        else:
            return None

    def build_paths(self):
        for _ in range(self.num_agents):
            start_lenght = len(self.grid.empty_cells) - len(self.starting_positions)
            if start_lenght > 0: #verifico di avere ancora celle libere per generare un nuovo agente
                new_path = self.__build_path()
                self.paths.append(new_path)
        return self.paths, self.starting_positions


    # def __is_collision_free(self, new_path: Path, current_paths: [Path]):
    #     # prendo come orizzonti temporali da controllari gli istanti di tempo che vanno da 0 a max, dove max ricordiamo
    #     # che può assumere come valore massimo la lunghezza massima dei percorsi già esistenti + la lunghezza del nuovo percorso
    #     for t in range(max([len(p) for p in current_paths] + [len(new_path)])):
    #         for path in current_paths:
    #             # vincolo 1: all'istante t, la medesima cella non può essere occupata da 2 agenti distinti
    #             if path[t] == new_path[t]:
    #                 print(1)
    #                 return False
    #             if t > 0:
    #                 # vincolo 2: due agenti che occupano celle adiacenti non possono scambiarsi il posto
    #                 if path[t] == new_path[t - 1] and new_path[t] == path[t - 1]:
    #                     print(2)
    #                     return False
    #
    #                 # vincolo 3: 2 agenti non possono incrociarsi durante il cambio cella
    #                 if new_path[t - 1][0] == path[t - 1][0] and new_path[t - 1][1] != path[t - 1][1]:
    #                     if new_path[t][0] == path[t][0] and new_path[t][1] != path[t][1]:
    #                         if new_path[t][1] == path[t - 1][1] and path[t][1] == new_path[t - 1][1]:
    #                             print(3)
    #                             return False
    #
    #                 if new_path[t - 1][1] == path[t - 1][1] and new_path[t - 1][0] != path[t - 1][0]:
    #                     if new_path[t][1] == path[t][1] and new_path[t][0] != path[t][0]:
    #                         if new_path[t][0] == path[t - 1][0] and path[t][0] == new_path[t - 1][0]:
    #                             print(4)
    #                             return False
    #     return True




