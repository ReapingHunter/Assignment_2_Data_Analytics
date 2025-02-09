import pandas as pd
from pySankey.sankey import sankey
import matplotlib.pyplot as plt
import os

# Construct the correct file path
script_dir = os.path.dirname(os.path.abspath(__file__))  
file_path = os.path.join(script_dir, "csv", "sankey_assignment.csv")

df = pd.read_csv(file_path)

# Define column groups
first_col = ["PEC", "NMCCC", "NRP", "NCDM", "RGS", "CNP", "PS", "OMP"]
second_col = ["S", "F", "D", "I", "N"]
third_col = ["Oth", "Reg", "Aca"]

df_melted1 = df.melt(id_vars=["LABEL"], value_vars=first_col, var_name="First", value_name="Value")
df_melted1 = df_melted1[df_melted1["Value"] > 0] 

df_melted2 = df.melt(id_vars=["LABEL"], value_vars=third_col, var_name="Third", value_name="Value")
df_melted2 = df_melted2[df_melted2["Value"] > 0]

df_merged = pd.merge(df_melted1, df_melted2, on="LABEL", suffixes=("_First", "_Third"))

fig = plt.figure(figsize=(14, 6))
manager = plt.get_current_fig_manager()
manager.window.geometry('1200x600')

orig_plt_figure = plt.figure

def force_main_figure(*args, **kwargs):
  return fig

ax1 = fig.add_subplot(1, 2, 1)
plt.sca(ax1)
plt.figure = force_main_figure
sankey(df_merged["First"], df_merged["LABEL"], aspect=20, fontsize=12)  # First → Second
ax1.set_title("First to LABEL Transition")
plt.figure = orig_plt_figure

ax2 = fig.add_subplot(1, 2, 2)
plt.sca(ax2)
plt.figure = force_main_figure
sankey(df_merged["LABEL"], df_merged["Third"], aspect=20, fontsize=12)  # Second → Third
ax2.set_title("LABEL to Third Transition")
plt.figure = orig_plt_figure

plt.tight_layout()
plt.show()