import csv
import logging
import matplotlib.pyplot as plt
import networkx as nx
import os
import sys
import timeit


current_index = 0
bridges = []

logging.basicConfig(filename='tarjan_times.log', level=logging.INFO)


def is_bridge(vertex_from, vertex_to):
    global bridges
    bridges.append((vertex_from, vertex_to))


def dfs(graph, used, tin, fup, vertex_from, vertex_to=-1):
    global current_index
    used[vertex_from] = True
    current_index += 1

    tin[vertex_from] = fup[vertex_from] = current_index

    for adj in graph[vertex_from]:
        if adj == vertex_to:  # coming back to the same parent node as we came from
            continue
        if used[adj]:
            fup[vertex_from] = min(fup[vertex_from], tin[adj])
        else:
            dfs(graph, used, tin, fup, adj, vertex_from)
            fup[vertex_from] = min(fup[vertex_from], fup[adj])
            if fup[adj] > tin[vertex_from]:
                is_bridge(vertex_from, adj)


def run_tarjan(init_graph, recursion_level=15000, sorted_edges=False):
    sys.setrecursionlimit(recursion_level)

    graph = init_graph
    used = {key: False for key in graph.keys()}
    tin = {key: None for key in graph.keys()}
    fup = {key: None for key in graph.keys()}

    for node in graph.keys():
        if not used[node]:
            dfs(graph, used, tin, fup, node)  # node=from
    if sorted_edges:
        logging.info("Bridges found: {}".format(sorted(bridges, key=lambda tup: tup[0])))
    else:
        logging.info("Number of bridges found: {}".format(len(bridges)))


# decorator to wrap function with arguments and return function without args for timeit
def wrapper(func, *args, **kwargs):
  def wrapped():
    return func(*args, **kwargs)
  return wrapped


def write_row(csv_file, data):

    if os.path.exists(csv_file_path):
        filemode = 'a'
    else:
        filemode = 'w'

    with open(csv_file, filemode) as csvfile:
        resultwriter = csv.writer(csvfile, delimiter=',', quotechar='|')
        resultwriter.writerow(data)


def draw_graph(graph, graph_name, save=True, positions=False):

    nx.write_edgelist(graph, path="grid.edgelist", delimiter=":")
    edge_list = nx.read_edgelist(path="grid.edgelist", delimiter=":")

    nx.draw(edge_list, with_labels=True)
    if positions:
        pos = nx.spring_layout(graph)  # positions for all nodes
        nx.draw_networkx_edges(graph, pos)
    if save:
        plt.savefig(os.path.join("graphs", graph_name))
    plt.show()


if __name__ == "__main__":

    csv_file_name = 'tarjan_results.csv'
    csv_file_path = os.path.join(os.getcwd(), csv_file_name)
    logging.info(csv_file_path)
    folder_path = os.path.join(os.getcwd(), "res")
    sub_dirs = next(os.walk(folder_path))[2]

    for filename in sub_dirs:
        logging.info("File: {}".format(filename))
        file_extension = os.path.splitext(filename)[-1].lower()
        logging.info(file_extension)

        if file_extension == ".adj_list":
            file_path = os.path.join(folder_path, filename)
            G = nx.read_adjlist(file_path)
            res = {}

            try:  # Python 2.6+
                res = nx.to_dict_of_lists(G)
            except TypeError:  # Python 3.x
                nx.write_adjlist(res, sys.stdout.buffer)  # write adjacency list to screen

            wrapped = wrapper(run_tarjan, res)
            bridges = []
            current_index = 0
            try:
                write_row(csv_file_path, [filename, str(timeit.timeit(wrapped, number=1))])
            except Exception as e:
                logging.error(e)
                continue