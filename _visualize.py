import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
data = pd.read_csv('output_full_norm.csv')

# Extract deadlines columns
deadlines = [col for col in data.columns if 'deadline' in col]

# Calculate mean values for disp and nodisp based on deadlines
mean_disp = data['disp'].mean()
mean_nodisp = data['nodisp'].mean()

# Plot
plt.figure(figsize=(10, 6))
for deadline in deadlines:
    plt.plot(data[deadline], data['disp'], label=f'disp - {deadline}', marker='o')
    plt.plot(data[deadline], data['nodisp'], label=f'nodisp - {deadline}', marker='o')

plt.axhline(mean_disp, color='blue', linestyle='--', label='Average disp')
plt.axhline(mean_nodisp, color='orange', linestyle='--', label='Average nodisp')
plt.legend()
plt.title('Disp and NoDisp based on Deadlines')
plt.xlabel('Deadlines')
plt.ylabel('Values')
plt.grid(True)
plt.tight_layout()
plt.show()