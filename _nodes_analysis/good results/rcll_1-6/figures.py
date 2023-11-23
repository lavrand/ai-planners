import pandas as pd
import matplotlib.pyplot as plt

TITLE_FONTSIZE = 50

FONTSIZE = 40

# Load the data from CSV files
time_data = pd.read_csv('Time.csv')
nodes_expanded_data = pd.read_csv('Nodes_Expanded.csv')

# Replace 'disp' with 'Dispatcher' in the dataframes
time_data.columns = time_data.columns.str.replace('disp', 'Dispatcher')
nodes_expanded_data.columns = nodes_expanded_data.columns.str.replace('disp', 'Dispatcher')

# Plotting the time taken by the Dispatcher approach for each problem instance
plt.figure(figsize=(TITLE_FONTSIZE, 10))
plt.bar(time_data['Identifier'], time_data['Dispatcher'], color='blue')
plt.xlabel('Problem Instance', fontsize=FONTSIZE)
plt.ylabel('Time (Seconds)', fontsize=FONTSIZE)
plt.title('Time Taken by Dispatcher Approach for Each Problem Instance', fontsize=TITLE_FONTSIZE)
plt.xticks(rotation=90, fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.grid(True)
plt.tight_layout()

# Saving the plot
time_taken_dispatcher_path = 'time_taken_disp.png'
plt.savefig(time_taken_dispatcher_path)
plt.close()

# For the Nodes Expanded graph
plt.figure(figsize=(TITLE_FONTSIZE, 10))
plt.bar(nodes_expanded_data['Identifier'], nodes_expanded_data['Dispatcher'], color='green')
plt.xlabel('Problem Instance', fontsize=FONTSIZE)
plt.ylabel('Nodes Expanded', fontsize=FONTSIZE)
plt.title('Nodes Expanded by Dispatcher Approach for Each Problem Instance', fontsize=TITLE_FONTSIZE)
plt.xticks(rotation=90, fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.grid(True)
plt.tight_layout()

# Saving the plot
nodes_expanded_dispatcher_path = 'nodes_expanded_disp.png'
plt.savefig(nodes_expanded_dispatcher_path)
plt.close()

time_taken_dispatcher_path, nodes_expanded_dispatcher_path