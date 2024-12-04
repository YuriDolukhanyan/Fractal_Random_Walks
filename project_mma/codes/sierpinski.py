import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx

def create_tree_graph(depth, branching_factor, start_node=0):
    G = nx.DiGraph()
    node_id = start_node
    nodes_at_current_depth = [node_id]
    for level in range(depth):
        next_nodes = []
        for parent in nodes_at_current_depth:
            for i in range(branching_factor):
                node_id += 1
                G.add_edge(parent, node_id)
                next_nodes.append(node_id)
        nodes_at_current_depth = next_nodes
    return G, node_id

def extend_graph_from_node(G, node, depth, branching_factor, current_max_id):
    new_subgraph, new_max_id = create_tree_graph(depth, branching_factor, start_node=current_max_id + 1)
    G.add_edges_from((node, child) for parent, child in new_subgraph.edges() if parent == current_max_id + 1)
    return new_max_id

def move_and_extend(start_node, G, steps=100, depth_to_extend=2, branching_factor=3):
    current_node = start_node
    path = []
    current_max_id = max(G.nodes)
    for _ in range(steps):
        neighbors = list(G.neighbors(current_node)) + list(G.predecessors(current_node))
        if neighbors:
            if not list(G.successors(current_node)):
                current_max_id = extend_graph_from_node(G, current_node, depth_to_extend, branching_factor, current_max_id)
            next_node = random.choice(neighbors)
            path.append((current_node, next_node))
            current_node = next_node
        else:
            break
    depths = [nx.dag_longest_path_length(G)] 
    return path, depths

N = 1000
result = []
for i in range(N):
    depth = 2
    branching_factor = 3
    steps = 10
    depth_to_extend = 2
    tree_graph, max_id = create_tree_graph(depth, branching_factor)
    start_node = 0
    random_walk_path, depths = move_and_extend(start_node, tree_graph, steps, depth_to_extend, branching_factor)
    print("Random Walk Path:")
    for edge in random_walk_path:
        print(edge)
    result.append(depths)

    print(i)
    # pos = nx.spring_layout(tree_graph, seed=42)
    # plt.figure(figsize=(10, 10))
    # nx.draw(tree_graph, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
    # edges = random_walk_path
    # nx.draw_networkx_edges(tree_graph, pos, edgelist=edges, edge_color='red', width=2)
    # plt.title(f"Tree Graph with Initial Depth {depth} and Branching Factor {branching_factor}")
    # plt.show()

print(result)
flattened_result = np.concatenate(result)
plt.figure(figsize=(10, 6))
plt.hist(flattened_result, bins=range(min(flattened_result), max(flattened_result) + 2), edgecolor='black', alpha=0.7)
plt.title("Histogram of Graph Depths")
plt.xlabel("Depth")
plt.ylabel("Frequency")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()