import os
from collections import OrderedDict

import matplotlib.pyplot as plt
import networkx as nx
import os
import sys
import timeit
# low_index = dict()
# index_node = dict()
# node_on_stack = dict()
# scc = list()

current_index = 0
bridges = []


# ToDO: add validation if the edge is not duplicated?
def is_bridge(vertex_from, vertex_to):
    global bridges
    bridges.append((vertex_from, vertex_to))
    # print("Bridge: {fromv} --> {to}".format(fromv=str(vertex_from), to=str(vertex_to)))


def dfs(graph, used, tin, fup, vertex_from, vertex_to=-1):
    global current_index
    used[vertex_from] = True
    current_index += 1
    # print("FROM: {fromv}".format(fromv=str(vertex_from)))
    # print("TO: {to}".format(to=str(vertex_to)))

    tin[vertex_from] = fup[vertex_from] = current_index
    # for node in graph.keys():
        # if !used[node]:
        #     dfs(graph, used, tin, fup, node)
    # print("graph[node]: ", graph[node])
    for adj in graph[vertex_from]:
        # print("Node: {node}, adj: {adj}".format(node=vertex_from, adj=adj))
        # print("used[{adjacent}]: {adj}".format(adj=used[adj], adjacent=str(adj)))
        if (adj == vertex_to):  # zeby nie wracac do rodzica wielokrotnie
            continue
        if used[adj]:
            # print("adjacent used!")
            fup[vertex_from] = min(fup[vertex_from], tin[adj])
        else:
            dfs(graph, used, tin, fup, adj, vertex_from)
            fup[vertex_from] = min(fup[vertex_from], fup[adj])
            if (fup[adj] > tin[vertex_from]):
                # print("fup[{adjacent}]: {adj}, tin[{current}]: {vfrom}".format(adj=fup[adj], vfrom=tin[vertex_from], adjacent=str(adj), current=str(vertex_from)))
                is_bridge(vertex_from, adj)


def run_tarjan(init_graph):
    sys.setrecursionlimit(15000)

    # graph = {'0': set(['1']),
    #          '1': set(['0', '2', '3']),
    #          '2': set(['1']),
    #          '3': set(['1', '4', '6']),
    #          '4': set(['3', '5']),
    #          '5': set(['4', '6']),
    #          '6': set(['3', '5'])}
    graph = init_graph
    used = {key: False for key in graph.keys()}
    tin = {key: None for key in graph.keys()}
    fup = {key: None for key in graph.keys()}

    for node in graph.keys():
        # print(node)
        if not used[node]:
            dfs(graph, used, tin, fup, node)  # node=from

    # print(sorted(bridges, key=lambda tup: tup[0]))
    print(len(bridges))



# decorator to wrap function with arguments and return function without args for timeit
def wrapper(func, *args, **kwargs):
  def wrapped():
    return func(*args, **kwargs)
  return wrapped


def draw_graph(G, graph_name, save=True):
    # run_tarjan(res)
    pos = nx.spring_layout(G)  # positions for all nodes

    nx.write_edgelist(G, path="grid.edgelist", delimiter=":")
    # read edgelist from grid.edgelist
    H = nx.read_edgelist(path="grid.edgelist", delimiter=":")

    nx.draw(H, with_labels=True)
    # nx.draw_networkx_edges(G, pos)
    if save:
        plt.savefig(os.path.join("graphs",graph_name))
    plt.show()

if __name__ == "__main__":

    # G = nx.barbell_graph(10, 10)
    # G = nx.complete_bipartite_graph(10,1)
    # G = nx.complete_graph(10)
    # G = nx.fast_gnp_random_graph(10, 0.2)
        # draw_graph(G, "random_10_02")
    file_path = os.path.join("res", "random_100000_02_36994.adj_list")
    print(file_path)
    G = nx.read_adjlist(file_path)
    # print(len(list(nx.bridges(G))))
    # print(list(nx.bridges(G)))

    res = {}
    try:  # Python 2.6+
        res = nx.to_dict_of_lists(G)
        # print(res)
        # nx.write_adjlist(res, sys.stdout)  # write adjacency list to screen
    except TypeError:  # Python 3.x
        nx.write_adjlist(res, sys.stdout.buffer)  # write adjacency list to screen

    wrapped = wrapper(run_tarjan, res)
    print(timeit.timeit(wrapped, number=1))

