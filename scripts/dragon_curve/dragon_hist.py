import seaborn as sns
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
iterations_to_extend = 3

result = []
for i in range(N):
    steps = 1000 # Number of steps for the random walk
    # Generate the initial Dragon Curve graph
    curve = generate_dragon_curve(iterations)
    dragon_graph = dragon_curve_to_graph(curve)
    start_node = 0
    # Perform the random walk and store the resulting depth
    _, depth, _ = move_and_extend_dragon(start_node, dragon_graph, steps, iterations_to_extend)
    result.append(depth)

    steps = 1001 # Number of steps for the random walk
    # Generate the initial Dragon Curve graph
    curve = generate_dragon_curve(iterations)
    dragon_graph = dragon_curve_to_graph(curve)
    start_node = 0
    # Perform the random walk and store the resulting depth
    _, depth, _ = move_and_extend_dragon(start_node, dragon_graph, steps, iterations_to_extend)
    result.append(depth)
    print(i)

# Define bin edges
bin_edges = [0, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 512]
bin_labels = [f"[{bin_edges[i]}, {bin_edges[i + 1]}]" for i in range(len(bin_edges) - 1)]

# Plot histogram
plt.figure(figsize=(10, 6))
freq, bins, _ = plt.hist(result, bins=bin_edges, edgecolor='black', alpha=0.7, label="Histogram", rwidth=0.9)

# Normalize KDE to align with frequency counts
kde = sns.kdeplot(result, color='red', linewidth=2, label="KDE")
kde_lines = kde.get_lines()[0]
kde_ydata = kde_lines.get_ydata()
kde_xdata = kde_lines.get_xdata()

# Scale KDE to match histogram frequencies
kde_scaled = kde_ydata * len(result) * (bin_edges[1] - bin_edges[0])
plt.plot(kde_xdata, kde_scaled, color='red', linewidth=2)

# Customize x-axis with bin labels
plt.xticks(ticks=[0.5 * (bin_edges[i] + bin_edges[i + 1]) for i in range(len(bin_edges) - 1)], labels=bin_labels, rotation=45)

plt.title(f"Histogram for Dragon Curve Fractal : n = {iterations}, Simulations = {N}, Steps per Simulation = {1000 & 1001} : Probabilty 3 to 1")
plt.xlabel("Depth Ranges")
plt.ylabel("Frequency")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()