import os
import csv
import subprocess
from datetime import datetime

# Directories to parse
directories = ['disp', 'nodisp']

# Base filename pattern
base_filename = "15-"

# Output CSV filename
csv_filename = "times.csv"


# Extract time from the line
def extract_time(line):
    try:
        return float(line.split()[2])
    except:
        return "N/A"


# Function to run a script and log its execution
def run_script(script_name):
    print(f"[{datetime.now()}] Starting {script_name}...")
    result = subprocess.run(['./' + script_name], check=True)
    print(f"[{datetime.now()}] Finished {script_name} with return code {result.returncode}")


# Ensure directories exist and have the correct permissions
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created {directory} directory.")
    os.chmod(directory, 0o755)
    print(f"Set permissions for {directory} to 755.")

# Running the scripts in the specified order
for script in ['gen', 'dispscript', 'nodispscript']:
    run_script(script)

# Main execution after scripts
with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write header to CSV
    csvwriter.writerow(['File', 'disp', 'nodisp'])

    for i in range(1, 101):  # 1 to 100 inclusive
        filename = base_filename + str(i)
        times = [filename]  # Start with filename as first column

        for directory in directories:
            filepath = os.path.join(directory, filename)

            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    # Read the file lines and filter for the line with '; Time'
                    line = next((l for l in f.readlines() if l.startswith("; Time")), None)

                    if line:
                        times.append(extract_time(line))
                    else:
                        times.append("N/A")
            else:
                times.append("N/A")

        # Write extracted times to CSV
        csvwriter.writerow(times)

print(f"Times extracted to {csv_filename}")
