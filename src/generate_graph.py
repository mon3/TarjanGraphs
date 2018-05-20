import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys
import timeit

nodes = 100000
probability = 0.00002

for i in range(1):
    G = nx.fast_gnp_random_graph(nodes, probability)
    res = {}
    try:
        res = nx.to_dict_of_lists(G)
    except TypeError:  # Python 3.x
        sys.stdout("Error")
        # nx.write_adjlist(res, sys.stdout.buffer)  # write adjacency list to screen
    size = len(list(nx.bridges(G)))
    file_name = "random_{}_02_{}.adj_list".format(nodes, size)
    file_path = os.path.join(os.getcwd(), '..', 'res', file_name)
    if os.path.exists(file_path):
        fh = open(file_path, 'wb')
    else:
        fh = open(file_path, 'wb+')
    nx.write_adjlist(G, fh)