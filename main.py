import sys
import timeout
from grid import Grid
from instance import Instance
from solver import Solver
from timeit import default_timer as timer
import psutil

def get_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    return memory_info.rss  # (bytes)

def read_cell(cell):
    cell = cell.replace(" ", "")
    x = int(cell[1])
    y = int(cell[3])
    return (x, y)

if __name__ == '__main__':
    # TODO:
    #  - aggiungere controlli che init e goal possano stare nella griglia
    #  - sistemare il plotting in modo da non avere sovrapposizioni
    #  - costruire un menu interattivo migliore

    if len(sys.argv) > 1:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        obstacle_percentage = float(sys.argv[3])
        conglomeration_ratio = float(sys.argv[4])
        grid = Grid(width, height, obstacle_percentage, conglomeration_ratio)

        init = read_cell(sys.argv[5])
        goal = read_cell(sys.argv[6])
        num_agents = int(sys.argv[7])
        max_length_agents = int(sys.argv[8])
        max_length = int(sys.argv[9])
        metric = int(sys.argv[10])
        time_limit = int(sys.argv[11])
    else:
        width = 500
        height = 500
        obstacle_percentage = 0.2
        conglomeration_ratio = 0.4
        grid = Grid(width, height, obstacle_percentage, conglomeration_ratio)

        init = grid.get_random_empty_cell()
        goal = grid.get_random_empty_cell()

        max_length_agents = 3
        num_agents = 1

        max_length = 1000
        metric = 0
        time_limit = 100


    try:
        with timeout.time_limit(time_limit):
            start = timer()

            istance = Instance(grid,
                               init,
                               goal,
                               max_length_agents,
                               num_agents)

            # parametro metric:
            # 0: distanza Euclidea
            # 1: distanza di Chebyshev
            resolver = Solver(istance, max_length, metric)
            path, num_expanded_states, inserted_states = resolver.solve()

            end = timer()
            execution_time = end - start

            #grid.print()
            istance.plot()

            if resolver.is_valid_start_stop():
                print("Percorso: ", path) if path is not None else print("Percorso: nessun percorso trovato")
            else:
                print("Percorso: Init e/o Goal sono sovrapposti ad un agente o ad un ostacolo")
            print("Numero di stati espansi: ", num_expanded_states)
            print("Numero di stati inseriti: ", inserted_states)
            print("Lunghezza del percorso: ", len(path) - 1) if path is not None else print("Lunghezza del percorso: 0")
            print(f"Costo del percorso: {istance.grid.get_path_cost(path):.3f}") if path is not None else print(
                "Costo del percorso: 0")
            print("Numero di mosse wait: ", istance.grid.get_num_waits(path)) if path is not None else print(
                "Numero di mosse wait: 0")
            print(f"Tempo di generazione della griglia: {istance.grid.execution_time:.3f} s")
            print(f"Tempo di generazione dell'istanza: {istance.execution_time:.3f} s")
            print(f"Tempo di risoluzione del problema: {execution_time:.3f} s")

            memory_used = get_memory_usage()
            print(f"Memoria utilizzata: {memory_used / (1024 * 1024):.2f} MB")

    except timeout.TimeoutException:
        print("Percorso: timeout, superato il tempo massimo per l'elaborazione")
        print("Numero di stati espansi: 0")
        print("Numero di stati inseriti: 0")
        print("Lunghezza del percorso: 0")
        print("Costo del percorso: 0")
        print("Numero di mosse wait: 0")
        print("Tempo di generazione della griglia: 0")
        print("Tempo di generazione dell'istanza: 0")
        print("Tempo di risoluzione del problema: 0")
        memory_used = get_memory_usage()
        print(f"Memoria utilizzata: {memory_used / (1024 * 1024):.2f} MB")
        sys.exit(2)


