import pandas as pd
import numpy as np

def calculate_log_etps_updated(nodes_expanded_file, time_file):
    # Read the CSV files
    nodes_expanded_df = pd.read_csv(nodes_expanded_file)
    time_df = pd.read_csv(time_file)

    # Merging the dataframes on 'Identifier'
    merged_df = pd.merge(nodes_expanded_df, time_df, on='Identifier', suffixes=('_nodes', '_time'))

    # Calculate Expanded Time Per Second (ETPS) for 'disp' and 'nodisp', while handling NaNs or 0 values
    merged_df['ETPS_disp'] = merged_df.apply(lambda row: row['disp_nodes'] / row['disp_time']
                                             if row['disp_time'] > 0 else np.nan, axis=1)
    merged_df['ETPS_nodisp'] = merged_df.apply(lambda row: row['nodisp_nodes'] / row['nodisp_time']
                                               if row['nodisp_time'] > 0 else np.nan, axis=1)

    # Concatenating the ETPS values from both 'disp' and 'nodisp', ignoring NaNs
    all_etps_values = pd.concat([merged_df['ETPS_disp'], merged_df['ETPS_nodisp']]).dropna()

    # Calculating the overall average ETPS
    overall_average_etps = all_etps_values.mean()

    # Log the overall average ETPS
    log_overall_average_etps = np.log(overall_average_etps) if overall_average_etps > 0 else 0

    return log_overall_average_etps

# Example usage
nodes_expanded_file = 'Nodes_Expanded.csv'  # Replace with your file path
time_file = 'Time.csv'  # Replace with your file path
log_etps = calculate_log_etps_updated(nodes_expanded_file, time_file)
print(f"Overall Average EPS: {log_etps}")
