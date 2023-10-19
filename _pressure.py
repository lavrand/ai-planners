import pandas as pd

# Load the data
data = pd.read_csv('output_full_norm.csv')


# Create difference columns and round to 2 decimal places
data['nodisp-disp'] = (data['nodisp'] - data['disp']).round(2)
data['deadline2-deadline1'] = (data['deadline2'] - data['deadline1']).round(2)
data['deadline3-deadline2'] = (data['deadline3'] - data['deadline2']).round(2)
data['deadline4-deadline3'] = (data['deadline4'] - data['deadline3']).round(2)
data['deadline5-deadline4'] = (data['deadline5'] - data['deadline4']).round(2)

# Calculate the sum of the differences for time_between_deadlines and round to 2 decimal places
data['time_between_deadlines'] = (data['deadline2-deadline1'] + data['deadline3-deadline2'] +
                                  data['deadline4-deadline3'] + data['deadline5-deadline4']).round(2)

# Write to new CSV file
data.to_csv('output_full_norm_pressure.csv', index=False)
