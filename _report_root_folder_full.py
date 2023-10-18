import os
import csv
import tarfile
import re

# Define the output file name
output_file_name = "output_full.csv"

# Ensure the directory is clean for the output file, avoiding appending to an old file.
if os.path.exists(output_file_name):
    os.remove(output_file_name)

# Write header to output file
with open(output_file_name, "w", newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["experiment", "File", "disp", "nodisp"] + [f"deadline{i}" for i in range(1, 9)])

def extract_deadlines(file_content):
    deadlines = []
    for line in file_content.splitlines():
        match = re.search(r'at (\d+\.\d+) \(not \(still-on-time package\d+\)\)', line)
        if match:
            deadlines.append(round(float(match.group(1)), 2))
    return deadlines

# Function to process tar.gz files
def process_tar_file(filepath, experiment_name):
    deadlines_dict = {}  # Holds extracted deadlines for each File

    with tarfile.open(filepath, "r:gz") as archive:
        for member in archive.getmembers():  # Use getmembers to ensure it's iterable
            if member.isreg():  # Ensure it's a regular file, not a folder
                file_name = os.path.basename(member.name)

                # Extract deadlines
                if file_name.startswith("withdeadlines-ontime-pfile"):
                    with archive.extractfile(member) as f:
                        content = f.read().decode("utf-8")
                        deadlines = extract_deadlines(content)
                        file_key = "-".join(file_name.split("-")[3:5])  # Extracting X-Y from pfileX-Y
                        deadlines_dict[file_key] = deadlines

                # Process times.csv
                elif member.name.endswith("times.csv"):
                    with archive.extractfile(member) as f:
                        file_content = f.read().decode("utf-8")
                        csv_reader = csv.reader(file_content.splitlines())
                        headers = next(csv_reader)  # Read the header row

                        if headers[:3] == ["File", "disp", "nodisp"]:
                            for row in csv_reader:
                                file_name, disp, nodisp = row
                                file_key = file_name.split(" ")[0]  # Extracting X-Y from 7-1 format
                                deadlines = deadlines_dict.get(file_key,
                                                               [None] * 8)  # Fill with None if no deadlines exist

                                with open(output_file_name, "a", newline='') as csvfile:
                                    csv_writer = csv.writer(csvfile)
                                    csv_writer.writerow([experiment_name, file_name, disp, nodisp] + deadlines)


# Start the traversal from specified directories
base_dirs = ["PC1", "PC2"]
for base in base_dirs:
    for root, dirs, files in os.walk(base):
        for file in files:
            match = re.match(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.tar\.gz)$", file)
            if match:
                experiment_name = match.group(1).split(".")[0]  # Extract the experiment name from the filename
                process_tar_file(os.path.join(root, file), experiment_name)

print(f"Data has been written to {output_file_name}")