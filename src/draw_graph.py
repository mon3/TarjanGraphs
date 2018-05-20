import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edges_from(
    [('v', 'c'), ('c', 'd'), ('c', 'e'), ('e', 'v')])

val_map = {'v': 1.0,
           'c': 0.5714285714285714,
           'e': 0.0}

values = [val_map.get(node, 0.25) for node in G.nodes()]

# Specify the edges you want here
red_edges = [('e', 'v')]
edge_colours = ['black' if not edge in red_edges else 'red'
                for edge in G.edges()]
black_edges = [edge for edge in G.edges() if edge not in red_edges]

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                       node_color = 'thistle', node_size = 1000)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=False, style='dashed')
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
plt.axis('off')

plt.savefig("example_graph.eps")
plt.show()