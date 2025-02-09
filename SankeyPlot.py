import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os

# Construct the correct file path
script_dir = os.path.dirname(os.path.abspath(__file__))  
file_path = os.path.join(script_dir, "csv", "sankey_assignment.csv")

df = pd.read_csv(file_path)