import networkx as nx
import networkx.algorithms.centrality as centrality
from pprint import pprint
import random

centralities = dict()
available_centralities = ['closeness', 'eigenvector', 'degree']
previous_node_types = dict()

def player_b_initialize(g):
    # This function is called once before the game starts.
    # Can be used for initializing auxiliary data of the player
    global available_centralities, previous_node_types
    centralities['eigenvector'] = centrality.eigenvector_centrality(g)
    centralities['closeness'] = centrality.closeness_centrality(g)
    centralities['degree'] = centrality.degree_centrality(g)
    previous_node_types = nx.get_node_attributes(g, "types")


def num_of_A_neighbors(g, neighbors, types, return_when_not_found=False, minimum=False):
    neighbors_A_count = { n:0 for n in neighbors}

    for n in neighbors:
        neighbors_of_neighbor = list(g.neighbors(n))
        for nn in neighbors_of_neighbor:
            if types[nn] == 'A':
                neighbors_A_count[n] += 1

    if max(neighbors_A_count.values()) == 0:
        if return_when_not_found:
            return neighbors[0]
        else:
            return None

    if minimum:
        return min(neighbors_A_count, key=neighbors_A_count.get)
    else:
        return max(neighbors_A_count, key=neighbors_A_count.get)


def based_on_centrality(neighbors, centrality, minimum=False):
    assert centrality in available_centralities, f'{centrality} not in available centralities. Check spelling'
    nodes = { n:score for n, score in centralities[centrality].items() if n in neighbors}
    if minimum:
        return min(nodes, key=nodes.get)
    else:
        return max(nodes, key=nodes.get)


def regain_lost_node(neighbors, current_node_types):
    global previous_node_types
    lost_node = None

    for node, attr in current_node_types.items():
        if previous_node_types[node] != attr:
            if previous_node_types[node] == 'B':
                lost_node = node
                break
    previous_node_types = current_node_types

    if lost_node and (lost_node in neighbors):
        return lost_node
    else:
        return None




def player_b_move(g, node) -> int:
    # This function is called everytime player b has been selected for a move
    node_types = nx.get_node_attributes(g, "types")
    neighbors = list(g.neighbors(node))
    a_neighbors = [n for n in neighbors if node_types[n] == 'A']


    # if there aren't any neighbors of type A return input node
    if not a_neighbors:
        return node

    # try to get back last round's lost node
    lost_node = regain_lost_node(a_neighbors, node_types)
    if lost_node: return lost_node

    # return neighbor with the least A neighbors or with the smallest centrality
    next_node = num_of_A_neighbors(g, a_neighbors, node_types, minimum=True)
    if next_node is None:
        return based_on_centrality(a_neighbors, 'closeness', minimum=True)
    else:
        return next_node
