import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to create a tree graph given depth and branching factor
def create_tree_graph(depth, branching_factor, start_node=0):
    G = nx.DiGraph()  # Directed graph
    node_id = start_node
    nodes_at_current_depth = [node_id]
    # Loop to build the tree based on the depth
    for _ in range(depth):
        next_nodes = []
        for parent in nodes_at_current_depth:
            for i in range(branching_factor):
                node_id += 1
                G.add_edge(parent, node_id)
                next_nodes.append(node_id) 
        nodes_at_current_depth = next_nodes # Move to the next depth
    return G, node_id # Return the graph and the current maximum node ID

# Function to extend the tree by adding a new subtree from a given node
def extend_graph_from_node(G, node, depth, branching_factor, current_max_id):
    # Create a new subtree with the specified depth and branching factor
    new_subgraph, new_max_id = create_tree_graph(depth, branching_factor, start_node=current_max_id + 1)
    # Add edges from the parent node to the new subtree
    G.add_edges_from((node, child) for parent, child in new_subgraph.edges() if parent == current_max_id + 1)
    return new_max_id

# Function to perform a random walk with dynamic tree extension
def move_and_extend(start_node, G, steps, depth_to_extend, branching_factor):
    current_node = start_node
    path = []
    current_max_id = max(G.nodes)
    for _ in range(steps):
        # Get all neighbors (successors and predecessors) of the current node
        neighbors = list(G.neighbors(current_node)) + list(G.predecessors(current_node))
        if neighbors:
            # If no successors, extend the graph by adding a subtree
            if not list(G.successors(current_node)):
                current_max_id = extend_graph_from_node(G, current_node, depth_to_extend, branching_factor, current_max_id)
            next_node = random.choice(neighbors)  # Choose a random neighbor
            path.append((current_node, next_node))
            current_node = next_node
        else:
            break # Break if no neighbors are available
    return path # Return the random walk path

# Initialize parameters
depth = 2 # Depth of the initial tree
branching_factor = 3 # Number of branches from each node
steps = 25 # Number of steps in the random walk
depth_to_extend = 2 # Depth to extend the tree at each step

# Create the initial tree graph and get the maximum node ID
tree_graph, max_id = create_tree_graph(depth, branching_factor)
start_node = 0  # Start the random walk from node 0
random_walk_path = move_and_extend(start_node, tree_graph, steps, depth_to_extend, branching_factor)

# Use Graphviz layout for tree structure visualization
pos = nx.nx_agraph.graphviz_layout(tree_graph, prog="dot") # Positioning for the tree layout
fig, ax = plt.subplots(figsize=(12, 8)) # Create a figure for the animation
edges_forward = [] # List to store forward edges
edges_backward = [] # List to store backward edges

# Update function for each frame of the animation
def update(frame):
    ax.clear()
    # Draw the graph with the current layout
    nx.draw(tree_graph, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray")
    
    # Loop to track forward and backward edges
    for i, edge in enumerate(random_walk_path[:frame + 1]):
        if edge[::-1] in edges_forward: # Check if the edge is a backward one
            edges_backward.append(edge) # Add to backward edges
        else:
            edges_forward.append(edge) # Add to forward edges

    # Draw forward edges in red
    nx.draw_networkx_edges(tree_graph, pos, edgelist=edges_forward, edge_color="red", width=2)
    # Draw backward edges in blue
    nx.draw_networkx_edges(tree_graph, pos, edgelist=edges_backward, edge_color="blue", width=2)

    # Update the title with the current step information
    current_edge = random_walk_path[frame]
    ax.set_title(f"Sierpinski Fractal Random Walk : Step {frame + 1}/{steps} - Current Edge: {current_edge}", fontsize=14)

# Save the animation as a GIF
ani = animation.FuncAnimation(fig, update, frames=len(random_walk_path), interval=250)  # Set frame update interval
ani.save("sierpinski_random_walk.gif", writer="imagemagick")  # Save as GIF using ImageMagick
plt.show()