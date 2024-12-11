import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# Function to generate the Dragon Curve up to a specified number of iterations
def generate_dragon_curve(iterations):
    # Initialize the curve with the first two points
    curve = [0 + 0j, 1 + 0j]
    for _ in range(iterations):
        # Generate the next segment by rotating and reversing
        curve_extension = [1j * (p - curve[-1]) + curve[-1] for p in reversed(curve[:-1])]
        curve.extend(curve_extension)
    return curve

# Convert the Dragon Curve into a graph representation
def dragon_curve_to_graph(curve):
    G = nx.Graph()
    # Add edges between consecutive points
    for i in range(len(curve) - 1):
        G.add_edge(i, i + 1)
    return G

# Simulate a random walk on the Dragon Curve graph with dynamic extension
def move_and_extend_dragon(start_node, G, steps, iterations_to_extend):
    current_node = start_node
    path = []
    visited_nodes = {current_node}

    # Perform the random walk for the given number of steps
    for _ in range(steps):
        neighbors = list(G.neighbors(current_node))
        if neighbors:
            # Extend the graph if needed
            if len(G.nodes) < (2 ** iterations_to_extend) + 1:
                curve = generate_dragon_curve(iterations_to_extend)
                dragon_graph = dragon_curve_to_graph(curve)
                G = nx.compose(G, dragon_graph)

            # Calculate weights for unvisited and visited neighbors
            weights = []
            for neighbor in neighbors:
                if neighbor not in visited_nodes:
                    weights.append(3) # Higher weight for unvisited neighbors
                else:
                    weights.append(1) # Lower weight for visited neighbors

            # Calculate probabilities for moving to each neighbor
            total_weight = sum(weights)
            probabilities = [w / total_weight for w in weights]
            next_node = random.choices(neighbors, weights=probabilities, k=1)[0]

            path.append((current_node, next_node))
            current_node = next_node
            visited_nodes.add(current_node)
        else:
            break

    # Calculate the diameter of the visited subgraph (for depth of the graph)
    visited_subgraph = G.subgraph(visited_nodes)
    depth = nx.diameter(visited_subgraph)
    return path, depth, G

# Simulation Parameters
N = 1000 # Number of simulations
iterations = 9 # Iterations for the initial Dragon Curve
steps = 2000 # Number of steps for the random walk
iterations_to_extend = 3

result = []
for i in range(N):
    # Generate the initial Dragon Curve graph
    curve = generate_dragon_curve(iterations)
    dragon_graph = dragon_curve_to_graph(curve)
    start_node = 0
    # Perform the random walk and store the resulting depth
    _, depth, _ = move_and_extend_dragon(start_node, dragon_graph, steps, iterations_to_extend)
    result.append(depth)
    print(i)

# Boxplot
plt.figure(figsize=(12, 6))
plt.boxplot(result, vert=False, patch_artist=True, notch=True,
            boxprops=dict(facecolor="lightblue", color="blue"),
            medianprops=dict(color="red", linewidth=2),
            whiskerprops=dict(color="blue", linewidth=1.5),
            capprops=dict(color="blue", linewidth=1.5),
            flierprops=dict(markerfacecolor='orange', marker='o', markersize=6))

# Adding Annotations
mean_depth = np.mean(result)
median_depth = np.median(result)

plt.axvline(mean_depth, color='green', linestyle='--', label=f"Mean: {mean_depth:.2f}")
plt.axvline(median_depth, color='red', linestyle='-', label=f"Median: {median_depth:.2f}")

# Adding Labels and Title
plt.title("Histogram for Dragon Curve Fractal : n = {9}, Iterations = {1000}, Steps per Iteration = {1000} : Probabilty 5 to 1")
plt.xlabel("Graph Depth")
plt.ylabel("Frequency")
plt.legend()
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()