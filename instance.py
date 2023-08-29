from grid import Grid
from agents import Agents
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from path import Path

class Instance:

    def __init__(self,
                 grid: Grid,
                 init: (int, int),
                 goal: (int, int),
                 max_lenght_agents, #lunghezza massima dei percorsi casuali da generare per gli agenti pre-esistenti
                 num_agents):

        start = timer()

        self.grid = grid
        self.init = init
        self.goal = goal
        self.num_agents = num_agents
        self.agent_generator = Agents(self.num_agents, self.grid, max_lenght_agents)

        end = timer()
        self.execution_time = end - start

    def plot(self):
        plt.close('all')
        self.grid.plot(show=False)
        plt.title(
            f'{self.grid.grid.shape[1]} x {self.grid.grid.shape[0]}\nObstacles: {self.grid.num_obstacles} / {self.grid.grid.size}')

        # stampo init e goal sulla griglia
        plt.plot(self.init[1] + 0.5, self.init[0] + 0.5, 'o', markersize=18, color='#ccc')
        plt.plot(self.goal[1] + 0.5, self.goal[0] + 0.5, 's', markersize=18, color='#ccc')

        plt.gca().set_prop_cycle(None)
        colors = ["red", "green", "blue", "purple", "orange", "pink", "cyan", "brown", "yellow"]
        tMax = max([len(p) for p in self.agent_generator.paths])
        for path in self.agent_generator.paths:
            index = self.agent_generator.paths.index(path)
            # quando il numero di agenti supera il numero di colori, andrò ad utilizzare gli stessi colori per agenti diversi
            color = colors[index % (len(colors))]
            for t in range(tMax + 1):
                if t < len(path):
                    plt.text(path[t][1] + 0.5, path[t][0] + 0.5, t, fontsize=12, color=color, ha='center', va='center')

        plt.show(block=False)

    def plot_instant(self, t, solution: Path):
        plt.close('all')
        self.grid.plot(show=False)
        plt.title(
            f'{self.grid.grid.shape[1]} x {self.grid.grid.shape[0]} - Obstacles: {self.grid.num_obstacles} / {self.grid.grid.size}\nIstant={t}')

        # stampo init e goal sulla griglia
        plt.plot(self.init[1] + 0.5, self.init[0] + 0.5, 'o', markersize=18, color='#ccc')
        plt.plot(self.goal[1] + 0.5, self.goal[0] + 0.5, 's', markersize=18, color='#ccc')

        plt.gca().set_prop_cycle(None)
        colors = ["red", "green", "blue", "purple", "orange", "pink", "cyan", "brown", "yellow"]
        for path in self.agent_generator.paths:
            index = self.agent_generator.paths.index(path)
            # quando il numero di agenti supera il numero di colori, andrò ad utilizzare gli stessi colori per agenti diversi
            color = colors[index % (len(colors))]
            plt.text(path[t][1] + 0.5, path[t][0] + 0.5, t, fontsize=12, color=color, ha='center', va='center')

        plt.plot(solution[t][1] + 0.5, solution[t][0] + 0.5, 'x', markersize=18)

        plt.show(block=False)