import pandas as pd
import matplotlib.pyplot as plt

FIGSIZE_Y = 20
FIGSIZE_X = 30

# Constants for font sizes
TITLE_FONTSIZE = 50
AXIS_FONTSIZE = 40
TICKS_FONTSIZE = 40

# Load the data from CSV files
time_data = pd.read_csv('Time.csv')
nodes_expanded_data = pd.read_csv('Nodes_Expanded.csv')

# Replace 'disp' with 'Dispatcher' in the dataframes
time_data.columns = time_data.columns.str.replace('disp', 'Dispatcher')
nodes_expanded_data.columns = nodes_expanded_data.columns.str.replace('disp', 'Dispatcher')

# Plotting the time taken by Dispatcher approach for each problem instance with improved figure size
plt.figure(figsize=(FIGSIZE_X, FIGSIZE_Y))  # Setting figure size
plt.bar(time_data['Identifier'], time_data['Dispatcher'], color='blue')
plt.xlabel('Problem Instance', fontsize=AXIS_FONTSIZE)
plt.ylabel('Time (Seconds)', fontsize=AXIS_FONTSIZE)
plt.title('Time Taken by Dispatcher Approach for Each Problem Instance', fontsize=TITLE_FONTSIZE)
plt.xticks(rotation=90, fontsize=TICKS_FONTSIZE)
plt.yticks(fontsize=TICKS_FONTSIZE)
plt.grid(True)
plt.tight_layout()

# Saving the plot
time_taken_dispatcher_path = 'time_taken_disp.png'
plt.savefig(time_taken_dispatcher_path)
plt.close()

# Plotting the nodes expanded by Dispatcher approach for each problem instance with improved figure size
plt.figure(figsize=(FIGSIZE_X, FIGSIZE_Y))  # Setting figure size
plt.bar(nodes_expanded_data['Identifier'], nodes_expanded_data['Dispatcher'], color='green')
plt.xlabel('Problem Instance', fontsize=AXIS_FONTSIZE)
plt.ylabel('Nodes Expanded', fontsize=AXIS_FONTSIZE)
plt.title('Nodes Expanded by Dispatcher Approach for Each Problem Instance', fontsize=TITLE_FONTSIZE)
plt.xticks(rotation=90, fontsize=TICKS_FONTSIZE)
plt.yticks(fontsize=TICKS_FONTSIZE)
plt.grid(True)
plt.tight_layout()

# Saving the plot
nodes_expanded_dispatcher_path = 'nodes_expanded_disp.png'
plt.savefig(nodes_expanded_dispatcher_path)
plt.close()

time_taken_dispatcher_path, nodes_expanded_dispatcher_path