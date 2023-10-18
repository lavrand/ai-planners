import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('output_full.csv')

# Remove rows where either 'disp' or 'nodisp' has a value of 9999
data = data[(data['disp'] != 9999) & (data['nodisp'] != 9999)]

# Remove rows where 'disp' or 'nodisp' is greater than 100
data = data[(data['disp'] <= 100) & (data['nodisp'] <= 100)]

# Save the cleaned data back to the CSV file
data.to_csv('output_full_cleaned.csv', index=False)
