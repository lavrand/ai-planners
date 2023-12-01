import pandas as pd
import numpy as np

# Read the Nodes_Expanded.csv file
nodes_expanded_df = pd.read_csv("Nodes_Expanded.csv")

# Define the constant EPS
EPS = 50

# Replace 'N/A' with np.nan and divide by EPS
nodes_expanded_df.replace('N/A', np.nan, inplace=True)
nodes_expanded_df[['disp', 'nodisp']] = nodes_expanded_df[['disp', 'nodisp']].apply(pd.to_numeric, errors='coerce') / EPS

# Sort the DataFrame based on Identifier
nodes_expanded_df.sort_values(by='Identifier', inplace=True)

# Save the Simulated_time.csv (before replacing NaNs with 9999)
simulated_time_df = nodes_expanded_df.fillna(9999)
simulated_time_df.to_csv("Simulated_Time.csv", index=False)

# Read the Solution.csv file
solution_df = pd.read_csv("Solution.csv")

# Preprocess Solution.csv to get the identifiers as integers
solution_df['Identifier'] = solution_df['Identifier'].str.split('-').str[0].astype(int)

# Update 'nodisp' in nodes_expanded_df based on Solution.csv criteria
for idx in solution_df.index:
    identifier = solution_df.at[idx, 'Identifier']
    if solution_df.at[idx, 'nodisp'] != 'Solution Found':
        nodes_expanded_df.loc[nodes_expanded_df['Identifier'] == identifier, 'nodisp'] = 9999

# Filter rows from Nodes_Expanded where 'disp' column in Solution.csv is 'Solution Found'
solution_identifiers = solution_df[solution_df['disp'] == 'Solution Found']['Identifier']
nodes_expanded_disp_solution_found_df = nodes_expanded_df[nodes_expanded_df['Identifier'].isin(solution_identifiers)]

# Replace NaNs with 9999 in the final result file
nodes_expanded_disp_solution_found_df.fillna(9999, inplace=True)

# Save the Nodes_Expanded_Disp_Solution_Found.csv
nodes_expanded_disp_solution_found_df.to_csv("Simulated_Time_Solution_Found.csv", index=False)
