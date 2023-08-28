import sys
import timeout
from grid import Grid
from instance import Instance
from solver import Solver
from timeit import default_timer as timer
import psutil
import csv
import numpy as np

def get_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    return memory_info.rss  # (bytes)

def get_record(width, height, obstacle_percentage, conglomeration_ratio, max_length, metric, time_limit, count):
    try:
        with (timeout.time_limit(time_limit)):
            start = timer()

            istance = Instance(grid,
                               init,
                               goal,
                               max_length_agents,
                               num_agents)
            resolver = Solver(istance, max_length, metric)
            path, num_expanded_states, inserted_states = resolver.solve()

            end = timer()
            execution_time = end - start
            memory_used = get_memory_usage()

            if path is not None:
                path_length = len(path) - 1
                path_cost = istance.grid.get_path_cost(path)
                num_waits = istance.grid.get_num_waits(path)
                grid_time = istance.grid.execution_time
                istance_time = istance.execution_time
                esito = "success"

            else:
                if resolver.is_valid_start_stop():
                    esito = "failure"
                else:
                    esito = "overlap"
                path_length = 0
                path_cost = 0
                num_waits = 0
                grid_time = 0
                istance_time = 0

            record = [count,
                      esito,
                      width,
                      height,
                      obstacle_percentage,
                      conglomeration_ratio,
                      max_length_agents,
                      num_agents,
                      max_length,
                      metric,
                      time_limit,
                      num_expanded_states,
                      inserted_states,
                      path_length,
                      float(f"{path_cost:.3f}"),
                      num_waits,
                      float(f"{grid_time:.2f}"),
                      float(f"{istance_time:.2f}"),
                      float(f"{execution_time:.2f}"),
                      float(f"{memory_used / (1024 * 1024):.2f}")]

    except timeout.TimeoutException:
        memory_used = get_memory_usage()
        esito = "timeout"
        record = [count,
                  esito,
                  width,
                  height,
                  obstacle_percentage,
                  conglomeration_ratio,
                  max_length_agents,
                  num_agents,
                  max_length,
                  metric,
                  time_limit,
                  0, 0, 0, 0, 0, 0, 0, 0,
                  float(f"{memory_used / (1024 * 1024):.2f}")]

    record = [str(item) for item in record]
    return record


if __name__ == '__main__':

    width_values = [4, 10, 100, 500]
    height_values = width_values
    obstacle_percentage_values = [0.2, 0.5, 0.9]
    conglomeration_ratio_values = [0.4, 0.7]
    max_length_agents_values = [3, 8, 20]
    num_agents_values = [1, 3, 10]
    max_length_values = [10, 100, 1000]
    metric_values = [0, 1]
    time_limit_values = [1, 10] #tempi in secondi

    n_iterarions = len(width_values) * len(height_values) * len(obstacle_percentage_values) * len(conglomeration_ratio_values) * len(max_length_agents_values) * len(num_agents_values) * len(max_length_values) * len(metric_values) * len(time_limit_values)

    nome_file = "/Users/davidezambelli/Desktop/data.csv"
    with open(nome_file, mode="w", newline="") as file_csv:
        writer = csv.writer(file_csv)
        head = ["id","outcome","width","height","obstacle_percentage","conglomeration_ratio","max_length_agents","num_agents","max_length","metric","time_limit","num_expanded_states","inserted_states","path_length","path_cost","num_waits","grid_time","istance_time","execution_time","memory_used"]
        file_csv.write(",".join(head) + "\n")

        count = -1
        for width in width_values:
            for height in height_values:
                for obstacle_percentage in obstacle_percentage_values:
                    for conglomeration_ratio in conglomeration_ratio_values:
                        grid = Grid(width, height, obstacle_percentage, conglomeration_ratio)
                        init = grid.get_random_empty_cell()
                        goal = grid.get_random_empty_cell()

                        for max_length_agents in max_length_agents_values:
                            for num_agents in num_agents_values:
                                for max_length in max_length_values:
                                    for metric in metric_values:
                                        for time_limit in time_limit_values:
                                            count += 1

                                            record = get_record(width, height, obstacle_percentage, conglomeration_ratio, max_length,
                                                                metric, time_limit, count)
                                            file_csv.write(",".join(record) + "\n")
                                            print(record)
                                            andamento = int(count / n_iterarions) * 100
                                            print(andamento, "%")
                                            if record[1] == "overlap":
                                                overlap_count = 0
                                                while record[1] == "overlap" and overlap_count < 5:
                                                    record = get_record(width, height, obstacle_percentage,
                                                                        conglomeration_ratio, max_length,
                                                                        metric, time_limit, count)
                                                    file_csv.write(",".join(record) + "\n")
                                                    print(record)
                                                    overlap_count += 1



