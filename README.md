# Random Walks on Complex Fractals  

## Overview  
This project explores **random walks on complex fractals**, focusing on the **Sierpiński Triangle** and the **Dragon Curve**. Random walks on fractals reveal intriguing mathematical properties, including non-standard scaling, self-similarity, and anomalous diffusion. This project implements algorithms to simulate random walks on these fractals and analyze their behavior.  

---

## Key Objectives  
1. Simulate random walks on the **Sierpiński Triangle** and **Dragon Curve**.  
2. Investigate the scaling behavior and fractal geometry of random walks.  
3. Visualize and analyze the diffusion characteristics specific to these fractals.  

---

## Features  
- **Fractal Generation**: Algorithms to construct fractals (Sierpiński Triangle and Dragon Curve).  
- **Random Walk Simulation**: Implementation of random walkers constrained to fractal geometries.  
- **Data Analysis**: Explore properties like mean squared displacement, scaling exponents, and path characteristics.  
- **Visualizations**: Plotting random walk paths, fractal structures, and statistical trends.  

---

## Prerequisites  
To run this project, ensure the following software/tools are installed:  
- **Python 3.8+**  
- Libraries:  
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `networkx`
  - `random`
# Dragon Curve Simulation and Analysis

This project simulates random walks on the Dragon Curve fractal and analyzes the resulting depths using histograms and kernel density estimation (KDE).

## Features
1. **Dragon Curve Generation**: Iteratively constructs the Dragon Curve fractal.
2. **Graph Representation**: Converts the curve into a graph structure using `networkx`.
3. **Dynamic Random Walk**: Simulates a random walk on the fractal graph, dynamically extending it as needed.
4. **Depth Analysis**: Analyzes the "depth" (diameter of visited subgraph) during the random walk.
5. **Visualization**: Visualizes the results using histograms and KDE plots with custom binning.

## Prerequisites
- Python 3.x
- Libraries: `seaborn`, `matplotlib`, `networkx`, `random`

Install the dependencies using:
```bash
pip install seaborn matplotlib networkx
```

## Parameters

- `N`: Number of simulations (default: 1000)
- `iterations`: Number of iterations to generate the initial Dragon Curve (2^n) (default: 9)
- `iterations_to_extend`: Number of iterations to use for graph extension during the walk (default: 3)
- `steps`: Number of steps per random walk (default: 1000 and 1001)

# Sierpinski Fractal Simulation and Analysis

This script simulates random walks on dynamically expanding tree graphs inspired by the Sierpinski fractal and visualizes the depth distribution using histograms and kernel density estimation (KDE).

## Features

1. **Tree Graph Generation**: Creates a directed tree graph with configurable depth and branching factor.
2. **Dynamic Graph Extension**: Extends the tree graph from specific nodes as needed during the random walk.
3. **Random Walk Simulation**: Simulates a random walk on the graph, exploring both successors and predecessors of each node.
4. **Depth Analysis**: Measures the depth (longest path length) of the tree graph during each simulation.
5. **Visualization**: Provides histogram and KDE plots for analyzing the depth distribution.

## Prerequisites

- Python 3.x
- Libraries: `random`, `networkx`, `seaborn`, `matplotlib`

Install the dependencies using:
```bash
pip install networkx seaborn matplotlib
```

## Parameters

- `N`: Number of simulations (default: 1000)
- `depth`: Initial depth of the tree (default: 2)
- `branching_factor`: Number of children per node (default: 3)
- `depth_to_extend`: Depth of tree extensions during the random walk (default: 2)
- `steps`: Number of steps per random walk (default: 1000 and 1001)
