import numpy as np
from scipy.stats import kstest
from mpmath import mp
from mpmath import meijerg
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

# Define the Tracy-Widom distribution (TW1) PDF using the Meijer G-function
def tracy_widom_pdf(x):
    pdf = []
    with mp.workdps(50): # High precision for numerical computation
        for val in x:
            if val > 0:
                # Calculate PDF using Meijer G-function
                result = meijerg([[], [0.5]], [[-0.5, 0], []], -val)
                pdf.append(float(mp.re(result)))  # Take only the real part
            else:
                pdf.append(0) # Tracy-Widom PDF is zero for non-positive values
    return np.array(pdf)

# Calculate the CDF from the PDF
def tracy_widom_cdf(x):
    pdf_vals = tracy_widom_pdf(x)
    cdf_vals = np.cumsum(pdf_vals) * (x[1] - x[0]) # Numerical integration for CDF
    return cdf_vals / cdf_vals[-1] # Normalize to make it a proper CDF

# Generate theoretical Tracy-Widom PDF values
x_vals = np.linspace(min(result), max(result), 500)
pdf_vals = tracy_widom_pdf(x_vals)

# Perform the Kolmogorov-Smirnov Test to compare the data with the Tracy-Widom distribution
cdf_vals = tracy_widom_cdf(x_vals)
ks_stat, p_value = kstest(result, lambda x: np.interp(x, x_vals, cdf_vals))
print(f"KS Statistic: {ks_stat}, P-value: {p_value}")

# Interpret the result of the KS test
if p_value > 0.05:
    print("The data is likely from the Tracy-Widom distribution (fail to reject H0).")
else:
    print("The data is not from the Tracy-Widom distribution (reject H0).")