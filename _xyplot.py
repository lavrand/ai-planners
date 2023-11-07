import csv
import os
import matplotlib.pyplot as plt
import sys

# Check if a command line argument has been provided
if len(sys.argv) < 2:
    print("Usage: python _xyplot.py <timeout>")
    sys.exit(1)

# The second command line argument is expected to be the config file name
MAX = sys.argv[1]

# Load the data from output_full.csv
data = []
with open('output_full.csv', 'r') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)  # Skip the header
    data = list(csv_reader)

# Extract disp and nodisp times, and set large values for '9999' and '99999'
disp_times_raw = [float(row[2]) for row in data]
nodisp_times_raw = [float(row[3]) for row in data]

valid_disp_times = [time for time in disp_times_raw if time not in [9999, 99999]]
valid_nodisp_times = [time for time in nodisp_times_raw if time not in [9999, 99999]]

# Calculate limits
# Check if valid_disp_times is empty, and use 60 as the default value if it is
max_disp = MAX if not valid_disp_times else max(valid_disp_times)
max_nodisp = MAX if not valid_nodisp_times else max(valid_nodisp_times)

# Replace 9999 and 99999 with the determined max values for plotting
disp_times = [time if time not in [9999, 99999] else max_disp for time in disp_times_raw]
nodisp_times = [time if time not in [9999, 99999] else max_nodisp for time in nodisp_times_raw]

# Create the xy-plot
plt.figure(figsize=(10, 8))
plt.scatter(disp_times, nodisp_times, color='blue', marker='o', alpha=0.5)

# Plot the line y=x, setting the color to red and increasing the line width.
max_limit = max(max_disp, max_nodisp)  # Ensuring the line spans the entire graph.
plt.plot([0, max_limit], [0, max_limit], color='red', linewidth=2)

# Settings for the plot with larger fonts.
font_size = 14  # You can adjust the size to your preference.
plt.title("Disp vs NoDisp Times", fontsize=font_size + 2)
plt.xlabel("Disp Time", fontsize=font_size)
plt.ylabel("NoDisp Time", fontsize=font_size)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Increase tick label size
plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)

# Set axes limits
plt.xlim(0, max_disp)
plt.ylim(0, max_nodisp)

# Save plot to file ensuring the layout is adjusted to include the bigger text.
plt.tight_layout()
plt.savefig("disp_vs_nodisp_plot.png")

print("Plot saved as disp_vs_nodisp_plot.png")
