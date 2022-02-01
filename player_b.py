import networkx as nx


def player_B_move(g, node) -> int:
    neighbors = g.neighbors(node)
    list_of_neighbors = list(neighbors)
    node_types = nx.get_node_attributes(g, "types")

    # Choose first foreign neighbor
    targets = [v for v in list_of_neighbors if node_types[v] != 'B']
    node = None
    if targets:
        node = targets[0]
    return node
