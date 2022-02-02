import networkx as nx


def player_b_initialize(g):
    # This function is called once before the game starts.
    # Can be used for initializing auxiliary data of the player
    pass


def player_b_move(g, node) -> int:
    # This function is called everytime player b has been selected for a move

    neighbors = g.neighbors(node)
    list_of_neighbors = list(neighbors)
    node_types = nx.get_node_attributes(g, "types")

    # Choose first foreign neighbor
    targets = [v for v in list_of_neighbors if node_types[v] != 'B']
    node = None
    if targets:
        node = targets[0]
    return node
