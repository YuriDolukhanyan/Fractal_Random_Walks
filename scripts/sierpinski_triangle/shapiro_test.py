import random
import networkx as nx
from scipy.stats import shapiro

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
steps = 1000 # Steps in the random walk
depth_to_extend = 2 # Depth of tree extensions

result = []
for i in range(N):
    tree_graph, max_id = create_tree_graph(depth, branching_factor)  # Create the initial tree graph
    start_node = 0  # Start the random walk at node 0
    random_walk_path, depths = move_and_extend(start_node, tree_graph, steps, depth_to_extend, branching_factor)
    result.extend(depths)  # Append depths to results
    print(i)

# Perform the Shapiro-Wilk test to assess normality of the results
stat, p_value = shapiro(result)

# Display the test results
print("Shapiro-Wilk Test Statistic:", stat)
print("P-value:", p_value)

# Interpret the test results
alpha = 0.05 # Significance level
if p_value > alpha:
    print("Data looks normally distributed (fail to reject H0)")
else:
    print("Data does not look normally distributed (reject H0)")