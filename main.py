import sys
import timeout
from grid import Grid
from instance import Instance
from solver import Solver
from timeit import default_timer as timer
import psutil
import re

def read_number(messaggio, min, max, type):
    while True:
        try:
            numero = type(input(messaggio))
            if max == None:
                if min <= numero:
                    return numero
                else:
                    print(f"Errore, il numero inserito dev'essere almeno pari a {min}")
            else:
                if min <= numero <= max:
                    return numero
                else:
                    print(f"Errore, il numero inserito dev'essere compreso tra {min} e {max} inclusi")
        except ValueError:
            if type == int:
                print("Errore, il valore inserito non è un numero intero")
            if type == float:
                print("Errore, il valore inserito non è un numero decimale")


def get_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    return memory_info.rss  # (bytes)

def read_cell(messaggio, grid: Grid):
    while True:
        cell = input(messaggio)
        cell = cell.replace(" ", "")
        pattern = r"\(\s*\d+\s*,\s*\d+\s*\)"
        if re.match(pattern, cell):
            x = int(cell[1])
            y = int(cell[3])
            if (x, y) in grid.get_G():
                return (x, y)
            else:
                print("Errore, la cella inserita non è valida")
        else:
            print("Errore, l'input inserito non è nella forma richiesta, la forma richiesta è (x,y)")

if __name__ == '__main__':


    mode = read_number("Seleziona la modalità di generazione del problema:\n"
                       "0: inserimento manuale dei parametri\n"
                       "1: generazione casuale mediante l'utilizzo dei parametri di default\n", 0, 1, int)

    if mode == 0:
        chose = 1
        while chose == 1:
            width = read_number("Inserire la larghezza della griglia: ", 1, None, int)
            height = read_number("Inserire l'altezza della griglia: ", 1, None, int)
            obstacle_percentage = read_number("Inserire la % di ostacoli che si desidera nella griglia: ", 0.0, 1.0, float)
            conglomeration_ratio = read_number("Inserire la % di conglomerazione degli ostacoli che si desidera nella griglia: ", 0.0, 1.0, float)
            grid = Grid(width, height, obstacle_percentage, conglomeration_ratio)
            grid.plot()
            chose = read_number("Questa è la griglia generata con ostacoli posizionati casualmente, scegliere un'opzione:\n"
                                "0: la griglia va bene, proseguire\n"
                                "1: la griglia NON va bene, generane una nuova\n", 0, 1, int)
        print("\nInserimento celle di partenza ed arrivo, N.B. la cella (0,0) è quella in alto a sinistra\n")
        init = read_cell("Inserie la cella di partenza del nuovo agente, nel formato (riga,colonna): ", grid)
        goal = read_cell("Inserie la cella di arrivo del nuovo agente, nel formato (riga,colonna): ", grid)

        num_agents = read_number("Inserie il numero di agenti pre-esistenti da inserire nella griglia: ", 0, None, int)
        max_length_agents = read_number("Inserie la massima lunghezza che dovranno avere i percorsi degli agenti pre-esistenti: ", 0, None, int)
        max_length = read_number("Inserire la lunghezza massima accettabile della soluzione del problema: ", 0, None, int)
        metric = read_number("Seleziona la metrica da utilizzare:\n"
                             "0: distanza Euclidea\n"
                             "1: distanza di Chebyshev\n", 0, 1, int)
        time_limit = read_number("Inserire il tempo massimo, in secondi, accettabile per calcolare la soluzione del problema: ", 0, None, int)

    else:
        width = 3
        height = 2
        obstacle_percentage = 0.2
        conglomeration_ratio = 0.4
        grid = Grid(width, height, obstacle_percentage, conglomeration_ratio)

        init = grid.get_random_empty_cell()
        goal = grid.get_random_empty_cell()

        max_length_agents = 1
        num_agents = 1

        max_length = 1000
        metric = 0
        time_limit = 100


    try:
        with timeout.time_limit(time_limit):


            istance = Instance(grid,
                               init,
                               goal,
                               max_length_agents,
                               num_agents)

            # parametro metric:
            # 0: distanza Euclidea
            # 1: distanza di Chebyshev
            resolver = Solver(istance, max_length, metric)

            start = timer()
            path, num_expanded_states, inserted_states = resolver.solve()
            end = timer()
            execution_time = end - start

            #grid.print()
            istance.plot()

            print("\n** Riassunto dell'istanza inserita: **")
            print("Dimensione griglia: ", width, " x ", height)
            print("Numero di celle attraversabili: ", width*height-int(width*height*obstacle_percentage))
            print("Percentuale di conglomerazione degli ostacoli: ", conglomeration_ratio, "%")
            print("Numero di agenti pre-esistenti: ", num_agents)
            print("Lunghezza massima dei percorsi degli agenti pre-esistenti: ", max_length_agents)
            print("Massima lunghezza accettabile per il percorso soluzione: ", max_length)
            print("Cella di partenza: ", init)
            print("Cella di arrivo: ", goal)
            metric_str = "Euclidea" if metric == 0 else "Chebyshev"
            print("Metrica utilizzata: ", metric_str)
            print("Limite massimo di tempo per la risoluzione del problema: ", time_limit, " secondi")

            print("\n** Esito dell'elaborazione: **")
            if resolver.is_valid_start_stop():
                print("Percorso: ", path) if path is not None else print("Percorso: nessun percorso trovato")
            else:
                print("Percorso: Init e/o Goal sono sovrapposti ad un agente o ad un ostacolo a causa della generazione casuale di alcuni parametri")
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

    if path is not None:
        t = 0
        while t != -1:
            t = read_number("\nInserire l'istante di cui si desidera visualizzare la situazione della griglia\n"
                            "Oppure digitare -1 per terminare il programma: ", -1, len(path) - 1, int)
            istance.plot_instant(t, path)
