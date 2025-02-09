import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

file_path = "./csv/networks_assignment.to_csv"
df = pd.read_csv(file_path)

df.columns = df.columns.str.strip().str.upper()
df["LABELS"] = df["LABELS"].str.strip().str.upper()

blue_nodes = {"D", "F", "I", "N", "S"}
green_nodes = {"BIH", "GEO", "ISR", "MNE", "SRB", "CHE", "TUR", "UKR", "GBR", "AUS", "HKG", "USA"}
yellow_nodes = {"AUT", "BEL", "BGR", "HRV", "CZE", "EST", "FRA", "DEU", "GRC", "HUN", "IRL",
                "ITA", "LVA", "LUX", "NLD", "PRT", "ROU", "SVK", "SVN", "ESP"}

# Allowed connections between central pentagram nodes
pentagram_edges = {("D", "S"), ("D", "F"), ("S", "N"), ("N", "I"), ("I", "F")}

G = nx.Graph()

for _, row in df.iterrows():
    node = row["LABELS"]
    G.add_node(node)

# Add edges based on adjacency matrix
for i, row in df.iterrows():
    node1 = row["LABELS"]
    for j, value in enumerate(row[1:]):
        node2 = df.columns[j + 1]

        # No edge on central nodes to other central nodes
        if (node1 in blue_nodes and node2 in blue_nodes) and (node1, node2) not in pentagram_edges and (node2, node1) not in pentagram_edges:
            continue
        
        if value > 0:
            G.add_edge(node1, node2, weight=value)

# Assign colors safely to avoid KeyErrors
node_colors = {}
for node in G.nodes:
    if node in blue_nodes:
        node_colors[node] = "deepskyblue"
    elif node in green_nodes:
        node_colors[node] = "green"
    elif node in yellow_nodes:
        node_colors[node] = "gold"
    else:
        node_colors[node] = "gray"

# Define pentagram positions
pentagram_positions = {
    "D": (0, 1), "S": (-0.95, 0.3), "N": (-0.6, -0.8),
    "I": (0.6, -0.8), "F": (0.95, 0.3)
}

# Generate positions for the other nodes
other_nodes = set(G.nodes) - set(pentagram_positions.keys())
angle_step = 2 * np.pi / max(1, len(other_nodes))
radius = 1.5
other_positions = {
    node: (radius * np.cos(i * angle_step), radius * np.sin(i * angle_step))
    for i, node in enumerate(other_nodes)
}

positions = {**pentagram_positions, **other_positions}

# Draw the graph
plt.figure(figsize=(8, 8))
nx.draw(G, pos=positions, with_labels=True, 
        node_color=[node_colors[node] for node in G.nodes],
        edge_color="black", node_size=1000, font_size=10, 
        font_color="white", font_weight="bold")

plt.title("Pentagram Network Graph with Additional Nodes")
plt.show()
