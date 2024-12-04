import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

def generate_dragon_curve(iterations):
    curve = [0 + 0j, 1 + 0j]
    for _ in range(iterations):
        curve_extension = [1j * (p - curve[-1]) + curve[-1] for p in reversed(curve[:-1])]
        curve.extend(curve_extension)
    return curve

def dragon_curve_to_graph(curve):
    G = nx.Graph()
    for i in range(len(curve) - 1):
        G.add_edge(i, i + 1)
    return G

def move_and_extend_dragon(start_node, G, steps, iterations_to_extend):
    current_node = start_node
    path = []
    visited_nodes = {current_node}

    for _ in range(steps):
        neighbors = list(G.neighbors(current_node))
        if neighbors:
            if len(G.nodes) < (2 ** iterations_to_extend) + 1:
                curve = generate_dragon_curve(iterations_to_extend)
                dragon_graph = dragon_curve_to_graph(curve)
                G = nx.compose(G, dragon_graph)

            # next_node = random.choice(neighbors)

            weights = []
            for neighbor in neighbors:
                if neighbor not in visited_nodes:
                    weights.append(3)
                else:
                    weights.append(1)

            total_weight = sum(weights)
            probabilities = [w / total_weight for w in weights]
            next_node = random.choices(neighbors, weights=probabilities, k=1)[0]

            path.append((current_node, next_node))
            current_node = next_node
            visited_nodes.add(current_node)
        else:
            break

    visited_subgraph = G.subgraph(visited_nodes)
    depth = nx.diameter(visited_subgraph)
    return path, depth, G

N = 1
result = []
for i in range(N):
    iterations = 10
    steps = 50
    iterations_to_extend = 3

    curve = generate_dragon_curve(iterations)
    dragon_graph = dragon_curve_to_graph(curve)
    start_node = 0
    random_walk_path, depths, extended_graph = move_and_extend_dragon(start_node, dragon_graph, steps, iterations_to_extend)

    print("Random Walk Path:")
    for edge in random_walk_path:
        print(edge)

    result.append(depths)
    print(i)
    pos = {i: (p.real, p.imag) for i, p in enumerate(curve)}
    plt.figure(figsize=(12, 8))
    nx.draw(extended_graph, pos, with_labels=False, node_size=10, edge_color='gray')
    nx.draw_networkx_edges(extended_graph, pos, edgelist=random_walk_path, edge_color='red', width=2)
    plt.title("Dragon Curve Graph with Random Walk Path")
    plt.show()

print(result)
plt.figure(figsize=(10, 6))
plt.hist(result, bins=range(min(result), max(result) + 2), edgecolor='black', alpha=0.7)
plt.title("Histogram of Graph Depths")
plt.xlabel("Depth")
plt.ylabel("Frequency")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()