import pandas as pd
import numpy as np

# Read the Nodes_Expanded.csv file
nodes_expanded_df = pd.read_csv("Nodes_Expanded.csv")

# Define the constant EPS
EPS = 10

# Replace 'N/A' with np.nan and divide by EPS
nodes_expanded_df.replace('N/A', np.nan, inplace=True)
nodes_expanded_df[['disp', 'nodisp']] = nodes_expanded_df[['disp', 'nodisp']].apply(pd.to_numeric, errors='coerce') / EPS

# Read the Solution.csv file
solution_df = pd.read_csv("Solution.csv")

# Preprocess Solution.csv to get the identifiers as integers
# Directly convert 'Identifier' to int, assuming they are numeric
solution_df['Identifier'] = solution_df['Identifier'].astype(int)

# Update disp and nodisp in nodes_expanded_df based on Solution.csv criteria
for idx in solution_df.index:
    identifier = solution_df.at[idx, 'Identifier']
    if solution_df.at[idx, 'disp'] != 'Solution Found':
        nodes_expanded_df.loc[nodes_expanded_df['Identifier'] == identifier, 'disp'] = 9999
    if solution_df.at[idx, 'nodisp'] != 'Solution Found':
        nodes_expanded_df.loc[nodes_expanded_df['Identifier'] == identifier, 'nodisp'] = 9999

# Sort the DataFrame based on Identifier
nodes_expanded_df.sort_values(by='Identifier', inplace=True)

# Save the Simulated_Time_Solution_Found.csv
# (Replacing NaNs with 9999 in the final result file)
nodes_expanded_df.fillna(9999, inplace=True)
nodes_expanded_df.to_csv("Simulated_Time_Solution_Found.csv", index=False)