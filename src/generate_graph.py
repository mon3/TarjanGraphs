import json
import networkx as nx
import os
import sys

nodes = 100000
probability = 0.000005


def generate_random_graph():
    """
    generates random graphs: external loop - number of repeated generations; inner loop-number of different probabilities

    :return: saves generated graphs to json and as networkx adjlist
    """
    for i in range(1, 100):
        for prob in range(1, 10):
            prob = float(prob / float(nodes*10))  # den=nodes*10
            G = nx.fast_gnp_random_graph(nodes, prob).to_undirected()
            res = {}
            try:
                res = nx.to_dict_of_lists(G)

            except TypeError:  # Python 3.x
                sys.stdout("Error")

            size = len(list(nx.bridges(G))) # number of bridges
            file_name_adj = "random_{}_{}_{}.adj_list".format(nodes, prob, size)
            file_name_json = "random_{}_{}_{}.json".format(nodes, prob, size)

            file_path_adj = os.path.join(os.getcwd(), '..', 'res', file_name_adj)
            file_path_json = os.path.join(os.getcwd(), '..', 'res', file_name_json)

            # writing to .json
            with open(file_path_json, "w") as f:
                json.dump(res, f, indent=4)

            # writing to .adjlist
            fh = open(file_path_adj, 'wb+')
            nx.write_adjlist(G, fh)


if __name__ == "__main__":
    generate_random_graph()

