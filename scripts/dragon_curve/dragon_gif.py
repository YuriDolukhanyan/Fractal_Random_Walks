import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
            # Dynamically extend the graph if not large enough
            if len(G.nodes) < (2 ** iterations_to_extend) + 1:
                curve = generate_dragon_curve(iterations_to_extend)
                dragon_graph = dragon_curve_to_graph(curve)
                G = nx.compose(G, dragon_graph)  # Merge the new graph with the existing one

            # Assign weights based on whether a neighbor is visited
            weights = []
            for neighbor in neighbors:
                if neighbor not in visited_nodes:
                    weights.append(3)  # Higher weight for unvisited neighbors
                else:
                    weights.append(1)  # Lower weight for visited neighbors

            # Calculate movement probabilities
            total_weight = sum(weights)
            probabilities = [w / total_weight for w in weights]
            next_node = random.choices(neighbors, weights=probabilities, k=1)[0]

            path.append((current_node, next_node))  # Record the edge in the path
            current_node = next_node
            visited_nodes.add(current_node)
        else:
            break

    # Measure the diameter of the visited subgraph
    visited_subgraph = G.subgraph(visited_nodes)
    depth = nx.diameter(visited_subgraph)
    return path, depth, G

# Main simulation setup
iterations = 9 # Number of iterations to generate the initial Dragon Curve
steps = 500 # Number of steps in the random walk
iterations_to_extend = 3 # Iterations for graph extension

# Generate the initial Dragon Curve and its graph
curve = generate_dragon_curve(iterations)
dragon_graph = dragon_curve_to_graph(curve)
start_node = 0

# Perform the random walk and graph extension
random_walk_path, depths, extended_graph = move_and_extend_dragon(start_node, dragon_graph, steps, iterations_to_extend)

# Output the random walk path
print("Random Walk Path:")
for edge in random_walk_path:
    print(edge)

result = [depths]
pos = {i: (p.real, p.imag) for i, p in enumerate(curve)}  # Map graph nodes to positions

# Animation setup
fig, ax = plt.subplots(figsize=(12, 8))

def update(frame):
    ax.clear()
    forward_edges = []
    backward_edges = []
    visited = set()

    # Separate edges into forward and backward for coloring
    for i, (u, v) in enumerate(random_walk_path[:frame + 1]):
        if v in visited:
            backward_edges.append((u, v))
        else:
            forward_edges.append((u, v))
        visited.add(v)

    # Draw the graph and edges
    nx.draw(extended_graph, pos, with_labels=False, node_size=10, edge_color='gray', ax=ax)
    nx.draw_networkx_edges(extended_graph, pos, edgelist=forward_edges, edge_color='red', width=2, ax=ax)
    nx.draw_networkx_edges(extended_graph, pos, edgelist=backward_edges, edge_color='blue', width=2, ax=ax)

    # Display current step and edge being traversed
    current_edge = random_walk_path[frame] if frame < len(random_walk_path) else None
    if current_edge:
        ax.set_title(f"Dragon Curve Graph with n = {iterations} : Random Walk Path - Step {frame + 1}/{steps}, Current Edge: {current_edge}")

# Save the animation as a GIF
ani = animation.FuncAnimation(fig, update, frames=len(random_walk_path), interval=50)
ani.save("dragon_curve_random_walk.gif", writer="imagemagick")
plt.show()
print(result)