import random
import sys
import time
import traceback

from collections import Counter

import networkx as nx
import matplotlib.pyplot as plt

from player_b import player_b_initialize
from player_b import player_b_move


class Parameters:
    n: int  # number of nodes
    m: int  # number of edges per new node (Barabasi-Albert)
    seed: int  # seed of random number generator
    interactive: bool  # flag: interactive execution, else batch execution

    # constructor
    def __init__(self, n, m, seed, interactive):
        self.n = n
        self.m = m
        self.seed = seed
        self.interactive = interactive

    def __repr__(self):
        return "Parameters()"

    def __str__(self):
        return f"n:{self.n}, m:{self.m}, seed:{self.seed}, interactive:{self.interactive}"


def get_number_of_types(g):
    node_types = nx.get_node_attributes(g, "types")
    type_values = [k[0] for k in node_types.values()]
    distinct_type_keys = Counter(type_values).keys()
    distinct_type_counts = Counter(type_values).values()

    # distinct_type_values = set(type_values)
    num_of_distinct_type_values = len(distinct_type_keys)
    return num_of_distinct_type_values, distinct_type_keys, distinct_type_counts


def draw_graph(g, node_pos):
    color_dict = {"A": "lightblue", "B": "red"}
    color_map = []
    node_types = nx.get_node_attributes(g, "types")
    for v in g.nodes:
        node_type = node_types[v]
        color = color_dict[node_type[0]]
        color_map.append(color)
    nx.draw(g, pos=node_pos, node_color=color_map, with_labels=True)
    plt.show()


def get_random_node(g, rng) -> int:
    num_of_nodes = g.number_of_nodes()
    node = rng.randint(0, num_of_nodes - 1)
    return node


def player_a_initialize(g):
    pass


def player_a_move(g, node) -> int:
    neighbors = g.neighbors(node)
    list_of_neighbors = list(neighbors)
    node_types = nx.get_node_attributes(g, "types")

    # Choose first foreign neighbor
    targets = [v for v in list_of_neighbors if node_types[v] != 'A']
    node = None
    if targets:
        node = targets[0]
    return node


def run_moran_game(p):
    # Create random number generator
    rng = random.Random(p.seed)

    # Create random graph
    G = nx.barabasi_albert_graph(p.n, p.m, rng.randint(0, 10000000))

    # Initial Assignment
    n = G.number_of_nodes()
    nodes_A = rng.sample(range(n), int(n / 2))
    set_A = set(nodes_A)
    nodes_B = list(set(range(n)) - set_A)
    set_B = set(nodes_B)

    types = []
    nx.set_node_attributes(G, types, "types")
    for v in G.nodes:
        if v in set_A:
            nx.set_node_attributes(G, {v: 'A'}, name="types")
        elif v in set_B:
            nx.set_node_attributes(G, {v: 'B'}, name="types")
        else:
            traceback.print_exc()
            sys.exit(f'Error: node {v} not in any set')

    # Initialize players

    player_b_initialize(G)

    # types.append("A")
    if p.interactive:
        pos = nx.spring_layout(G)

    step = 0
    while True:
        random_node = get_random_node(G, rng)
        types = nx.get_node_attributes(G, "types")
        node_type = types[random_node][0]

        if node_type == 'A':
            move = player_a_move(G, random_node)
        elif node_type == 'B':
            move = player_b_move(G, random_node)
            if move not in list(G.neighbors(random_node)):
                raise Exception(f'Invalid move: Node {move} is not a neighbor of node {random_node}')
        else:
            traceback.print_exc()
            sys.exit(f'Error: unexpected type: {type}')

        nx.set_node_attributes(G, {move: node_type}, name="types")
        num_of_types, distinct_keys, distinct_counts = get_number_of_types(G)
        step += 1

        if p.interactive:
            draw_graph(G, pos)
            # input("Press Enter to continue...")
            time.sleep(0.1)

        if num_of_types == 1:
            print(f'Parameters {p}, Fixation {distinct_keys} after {step} number of steps!')
            return list(distinct_keys)[0], step


run_moran_game(Parameters(20, 2, 123, False))
run_moran_game(Parameters(30, 2, 123, False))
run_moran_game(Parameters(50, 2, 123, False))
run_moran_game(Parameters(150, 2, 123, False))
run_moran_game(Parameters(200, 2, 123, False))
run_moran_game(Parameters(500, 2, 123, False))
run_moran_game(Parameters(1000, 2, 123, False))
run_moran_game(Parameters(1000, 4, 123, False))
run_moran_game(Parameters(1000, 5, 123, False))
run_moran_game(Parameters(1000, 5, 345, False))
