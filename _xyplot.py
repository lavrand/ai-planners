import csv
import os
import matplotlib.pyplot as plt

# Load the data from output_full.csv
data = []
with open('output_full.csv', 'r') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)  # Skip the header
    data = list(csv_reader)

# Extract disp and nodisp times, and set large values for '9999' and '99999'
disp_times_raw = [float(row[1]) for row in data]
nodisp_times_raw = [float(row[2]) for row in data]

valid_disp_times = [time for time in disp_times_raw if time not in [9999, 99999]]
valid_nodisp_times = [time for time in nodisp_times_raw if time not in [9999, 99999]]

# Calculate limits
max_disp = max(valid_disp_times)
max_nodisp = max(valid_nodisp_times)

# Replace 9999 and 99999 with the determined max values for plotting
disp_times = [time if time not in [9999, 99999] else max_disp for time in disp_times_raw]
nodisp_times = [time if time not in [9999, 99999] else max_nodisp for time in nodisp_times_raw]

# Create the xy-plot
plt.figure(figsize=(10, 8))
plt.scatter(disp_times, nodisp_times, color='blue', marker='o', alpha=0.5)

# Settings for the plot
plt.title("Disp vs NoDisp Times")
plt.xlabel("Disp Time")
plt.ylabel("NoDisp Time")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Set axes limits
plt.xlim(0, max_disp)
plt.ylim(0, max_nodisp)

# Save plot to file
plt.tight_layout()
plt.savefig("disp_vs_nodisp_plot.png")

print("Plot saved as disp_vs_nodisp_plot.png")
