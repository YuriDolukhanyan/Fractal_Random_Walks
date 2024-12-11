import random
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt

# Function to create a tree graph with a given depth and branching factor
def create_tree_graph(depth, branching_factor, start_node=0):
    G = nx.DiGraph() # Create a directed graph to represent the tree
    node_id = start_node # Initialize the node ID
    nodes_at_current_depth = [node_id]  # Nodes at the current depth level
    for level in range(depth):
        next_nodes = []
        for parent in nodes_at_current_depth:
            for i in range(branching_factor):
                node_id += 1
                G.add_edge(parent, node_id) # Add edges from parent to child
                next_nodes.append(node_id)
        nodes_at_current_depth = next_nodes # Move to the next depth level
    return G, node_id

# Function to extend the graph by adding a new sub-tree from a specific node
def extend_graph_from_node(G, node, depth, branching_factor, current_max_id):
    # Generate a new subgraph and connect it to the given node
    new_subgraph, new_max_id = create_tree_graph(depth, branching_factor, start_node=current_max_id + 1)
    G.add_edges_from((node, child) for parent, child in new_subgraph.edges() if parent == current_max_id + 1)
    return new_max_id

# Perform a random walk and dynamically extend the graph as needed
def move_and_extend(start_node, G, steps=100, depth_to_extend=2, branching_factor=3):
    current_node = start_node
    path = [] # Store the path of the random walk
    current_max_id = max(G.nodes)  # Track the current maximum node ID
    for _ in range(steps):
        neighbors = list(G.neighbors(current_node)) + list(G.predecessors(current_node))
        if neighbors:
            # Extend the graph if the current node has no successors
            if not list(G.successors(current_node)):
                current_max_id = extend_graph_from_node(G, current_node, depth_to_extend, branching_factor, current_max_id)
            # Randomly choose the next node
            next_node = random.choice(neighbors)
            path.append((current_node, next_node))
            current_node = next_node
        else:
            break
    # Measure the longest path length in the graph (depth)
    depths = [nx.dag_longest_path_length(G)]
    return path, depths

# Simulation parameters
N = 1000 # Number of random walks to simulate
depth = 2 # Initial depth of the tree
branching_factor = 3 # Number of children for each node
depth_to_extend = 2 # Depth of tree extensions

result = []
for i in range(N):
    steps = 1000 # Steps in the random walk
    tree_graph, _ = create_tree_graph(depth, branching_factor)  # Create the initial tree graph
    start_node = 0  # Start the random walk at node 0
    _, depths = move_and_extend(start_node, tree_graph, steps, depth_to_extend, branching_factor)
    result.extend(depths)  # Append depths to results

    steps = 1001 # Steps in the random walk
    tree_graph, _ = create_tree_graph(depth, branching_factor)  # Create the initial tree graph
    start_node = 0  # Start the random walk at node 0
    _, depths = move_and_extend(start_node, tree_graph, steps, depth_to_extend, branching_factor)
    result.extend(depths)  # Append depths to results

    print(i)

# Plotting the histogram and KDE
plt.figure(figsize=(10, 6))

# Plot histogram of depths
freq, bins, _ = plt.hist(result, bins=range(min(result), max(result) + 2),
                         edgecolor='black', alpha=0.7, label="Histogram", rwidth=0.9)

# KDE (Kernel Density Estimation) plot for smoother visualization
kde = sns.kdeplot(result, color='red', linewidth=2, label="KDE")
kde_lines = kde.get_lines()[0]  # Get the KDE line
kde_ydata = kde_lines.get_ydata()
kde_xdata = kde_lines.get_xdata()

# Scale KDE to align with histogram frequencies
kde_scaled = kde_ydata * len(result) * (bins[1] - bins[0])
plt.plot(kde_xdata, kde_scaled, color='red', linewidth=2)  # Plot scaled KDE

# Customize the plot
plt.title(f"Histogram for Sierpinski Fractal : Simulations = {N}, Steps per Simulation = {1000 & 1001}")
plt.xlabel("Depth")
plt.ylabel("Frequency")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()