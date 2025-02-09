import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import os

# Construct the correct file path
script_dir = os.path.dirname(os.path.abspath(__file__))  
file_path = os.path.join(script_dir, "csv", "bar_assignment.csv")  

# Read CSV
df = pd.read_csv(file_path)

# Aggregate: Count occurrences of each (LABEL, COUNT) pair
df_grouped = df.groupby(['LABEL', 'COUNT']).size().unstack(fill_value=0)

# Define colors: Red for '0', Blue for '1'
colors = {0: 'red', 1: 'blue'}

# Create horizontal stacked bar chart
fig, ax = plt.subplots(figsize=(8, 5))
bars_0 = ax.barh(df_grouped.index, df_grouped[0], color=colors[0], label='No')
bars_1 = ax.barh(df_grouped.index, df_grouped[1], left=df_grouped[0], color=colors[1], label='Yes')

# Add text inside bars (aligned to the right)
for bars, count_value in [(bars_0, 0), (bars_1, 1)]:
    for bar in bars:
        width = bar.get_width()
        if width > 0:  # Avoid placing text in empty bars
            ax.text(
                bar.get_x() + width - 0.4,
                bar.get_y() + bar.get_height() / 2, 
                str(int(width)), 
                ha='center',
                va='center', 
                color='white', 
                fontsize=14, 
                fontweight='bold'
            )

# Labels and title
ax.set_xlabel("Count", fontsize=14, fontweight="bold")
ax.set_ylabel("Label", fontsize=14, fontweight="bold")
ax.set_title("Horizontal Stacked Bar Chart", fontsize=14, fontweight="bold", pad=30)

# Create custom legend handles
red_square = mlines.Line2D([], [], marker='s', color='red', label='No', markersize=10, linewidth=0)
blue_square = mlines.Line2D([], [], marker='s', color='blue', label='Yes', markersize=10, linewidth=0)

# Add the custom legend at the bottom of the title
ax.legend(handles=[red_square, blue_square], loc='upper left', bbox_to_anchor=(0.01, 1.1), ncol=2, fontsize=14, frameon=False)

ax.grid(False)
ax.tick_params(axis='both', which='major', labelsize=12, width=2)

# Show the plot
plt.show()
