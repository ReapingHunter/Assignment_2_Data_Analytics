import pandas as pd
import plotly.graph_objects as go
import os

# Construct the correct file path
script_dir = os.path.dirname(os.path.abspath(__file__))  
file_path = os.path.join(script_dir, "csv", "sankey_assignment.csv")

df = pd.read_csv(file_path)

# Define column groups
first_col = ["PEC", "NMCCC", "NRP", "NCDM", "RGS", "CNP", "PS", "OMP"]
third_col = ["Oth", "Reg", "Aca"]

# Melt the dataframes to restructure them
df_melted1 = df.melt(id_vars=["LABEL"], value_vars=first_col, var_name="First", value_name="Value")
df_melted1 = df_melted1[df_melted1["Value"] > 0] 

df_melted2 = df.melt(id_vars=["LABEL"], value_vars=third_col, var_name="Third", value_name="Value")
df_melted2 = df_melted2[df_melted2["Value"] > 0]

# Merge both dataframes
df_merged = pd.merge(df_melted1, df_melted2, on="LABEL", suffixes=("_First", "_Third"))

# Create mapping for node labels
unique_labels = list(df_merged["First"].unique()) + list(df_merged["LABEL"].unique()) + list(df_merged["Third"].unique())
unique_labels = list(set(unique_labels))  # Remove duplicates

# Create the indices for source, target, value, and color in the Sankey diagram
source = []
target = []
value = []

# Define a color palette for the nodes
node_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', 
    '#bcbd22', '#17becf', '#6a51a3', '#de2d26', '#31a354', '#fdae61', '#b3de69', '#636363', 
    '#ffcb00', '#ff6f00', '#bc2a8d', '#7fa4b2', '#F79C42', '#A1C6EA', '#D4AF37', '#AD4A2D', 
    '#E9A7C0', '#D32F2F', '#2D7DD2', '#7FB800', '#9C4D4D', '#9C27B0', '#7B1FA2'
]

node_color_mapping = {}

# Map 'First', 'LABEL', and 'Third' to indices in the labels
for idx, label in enumerate(unique_labels):
    node_color_mapping[label] = node_colors[idx % len(node_colors)]  # Assign a unique color to each label

# Create a color list for links (links will have the color of their source node)
link_colors = []
link_pairs = set()  # Use a set to track already added link pairs

for _, row in df_merged.iterrows():
    # First to LABEL (outgoing link will have the same color as the source)
    link_pair_1 = (row["First"], row["LABEL"])
    if link_pair_1 not in link_pairs:
        source.append(unique_labels.index(row["First"]))
        target.append(unique_labels.index(row["LABEL"]))
        value.append(row["Value_First"])  # Value from First to LABEL
        link_colors.append(node_color_mapping[row["First"]])  # Link color matches source node color
        link_pairs.add(link_pair_1)

    # LABEL to Third (outgoing link will have the same color as the source)
    link_pair_2 = (row["LABEL"], row["Third"])
    if link_pair_2 not in link_pairs:
        source.append(unique_labels.index(row["LABEL"]))
        target.append(unique_labels.index(row["Third"]))
        value.append(row["Value_Third"])  # Value from LABEL to Third
        link_colors.append(node_color_mapping[row["LABEL"]])  # Link color matches source node color
        link_pairs.add(link_pair_2)

# Create the Sankey diagram with colored nodes and links
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=unique_labels,
        color=[node_color_mapping[label] for label in unique_labels],  # Set node colors
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=link_colors,  # Set link colors to match the source node
    )
))

# Update layout
fig.update_layout(
    title_text="Sankey Plot",
    font_size=12,
    width=1200,
    height=600
)

# Show the figure
fig.show()
