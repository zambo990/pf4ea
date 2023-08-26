import numpy as np
from typing import Callable
from instance import Instance
from path import Path

class Solver:

    def __init__(self, istance: Instance, max_lenght): #TODO aggiungere il parametro heuristic
        self.istance = istance
        self.max_length = max_lenght
        if self.max_length > self.__maximum_max_length(self.istance.agent_generator.max_length):
            self.max_length = self.__maximum_max_length(self.istance.agent_generator.max_length)

    def __maximum_max_length(self, agent_path_length):
        return agent_path_length + (self.istance.grid.grid.size - self.istance.grid.num_obstacles)

    def __h(self, v: (int, int), goal: (int, int)):
        dx = abs(v[1] - goal[1])
        dy = abs(v[0] - goal[0])
        return dx + dy + (np.sqrt(2) - 2) * min(dx, dy)

    def solve(self):
        if not self.__is_valid_start_stop():
            return None, 0, 0
        return self.reach_goal()

    def reach_goal(self):
        # (parte 1): inizializzazione delle strutture dati: sono stati scelti i dizionari in quanto vengono fatte molte
        # operazioni di ricerca, di conseguenza è la struttura migliore

        inserted_states = 1
        agents = self.istance.agent_generator
        G = self.istance.grid.get_G()
        closed = set()
        open = {(self.istance.init, 0)}
        g = {}
        P = {}
        f = {}
        g[(self.istance.init, 0)] = 0
        f[(self.istance.init), 0] = self.__h(self.istance.init, self.istance.goal)

        # (parte 2): estrazione di uno stato da oper per controllare l'eventuale raggiungimento di goal
        while len(open) != 0:
            min_state = self.__extract_min_state(open, lambda v: f[v] if v in f else np.inf)
            v, t = min_state
            open = open - {(v, t)}
            closed = closed | {(v, t)}
            if v == self.istance.goal:
                return self.__reconstruct_path(P, t), len(closed), inserted_states

            # (parte 3): verifica che non si oltrepassi l'orizzonte temporale e che non si presentino collisioni
            if t < self.max_length:
                adj = G
                for n in adj[v]:
                    n, _ = n #ricavo solo il vertice (ignoro il costo associato)
                    if (n, t + 1) not in closed:
                        traversable = True
                        for a in agents.paths:
                            if (a[t+1] == n) or (a[t+1] == v and a[t] == n):
                                traversable = False
                            else: #aggiungo il controllo che verifica che non vi siano incroci diagonali
                                # vertice v: vertice da cui parte il nuovo agente (tempo t)
                                # vertice n: vertice di arrivo del nuovo agente (tempo t+1)

                                # a[t]: vertice attuale dell'agente pre-esistente
                                # a[t+1]: vertice successivo dell'agente pre-esistente

                                if v[0] == a[t][0] and v[1] != a[t][1]:
                                    if n[0] == a[t+1][0] and n[1] != a[t+1][1]:
                                        if n[1] == a[t][1] and a[t+1][1] == v[1]:
                                            traversable = False

                                if v[1] == a[t][1] and v[0] != a[t][0]:
                                    if n[1] == a[t+1][1] and n[0] != a[t+1][0]:
                                        if n[0] == a[t][0] and a[t+1][0] == v[0]:
                                            traversable = False
                        # (parte 4): aggiorna P e g ed inserisce il nuovo stato in open;
                        # restituisce "fallimento" nel caso la lista open si svuoti
                        if traversable:
                            if (n, t + 1) not in g or g[(v, t)] + self.istance.grid.get_W(v, n) < g[(n, t + 1)]:
                                P[(n, t + 1)] = (v, t)
                                g[(n, t + 1)] = g[(v, t)] + self.istance.grid.get_W(v, n)
                                f[(n, t + 1)] = g[(n, t + 1)] + self.__h(n, self.istance.goal)
                            if (n, t + 1) not in open:
                                open = open | {(n, t + 1)}
                                inserted_states += 1
        return None, len(closed), inserted_states

    def __extract_min_state(self, open, function: Callable[[(int, int)], float]):
        min_el = next(iter(open))
        min_score = function(min_el)
        for el in open:
            score = function(el)
            if score < min_score:
                min_score = score
                min_el = el
        return min_el

    def __reconstruct_path(self, P, t: int) -> Path:
        path = Path([self.istance.goal])
        while path[-1] != self.istance.init or t != 0:
            previous = P[(path[-1], t)]
            path.append(previous[0])
            t -= 1
        path.reverse()
        return path

    def __is_valid_start_stop(self):
        # caso in cui init coincide con la posizione iniziale di uno degli agenti pre-esistenti
        if self.istance.init in self.istance.agent_generator.starting_positions:
            return False
        # caso in cui il goal coincide con una delle posizioni finali degli agenti pre-esistenti
        for path in self.istance.agent_generator.paths:
            if self.istance.goal == path[-1]:
                return False
        # caso in cui init coincida con uno degli ostacoli generati casualmente
        if self.istance.init not in self.istance.grid.get_G():
            return False

        return True


