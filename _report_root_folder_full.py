import os
import csv
import tarfile
import re

# Define the output file name
output_file_name = "output_full.csv"

# Write header to output file
with open(output_file_name, "w") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["experiment", "disp", "nodisp"])

# Function to process zip files
def process_zip_file(filename, experiment_name):
    with tarfile.open(filename, "r:gz") as archive:
        for member in archive:
            if member.name.endswith("times.csv"):
                with archive.extractfile(member) as f:
                    file_content = f.read().decode("utf-8")
                    csv_reader = csv.reader(file_content.splitlines())
                    next(csv_reader)  # Skip header
                    for row in csv_reader:
                        disp, nodisp = row[1], row[2]
                        with open(output_file_name, "a") as csvfile:
                            csv_writer = csv.writer(csvfile)
                            csv_writer.writerow([experiment_name, disp, nodisp])

# Start the traversal from current directory
base_dirs = ["PC1", "PC2"]
for base in base_dirs:
    for root, dirs, files in os.walk(base):
        for file in files:
            match = re.match(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.tar\.gz$", file)
            if match:
                experiment_name = match.group(1)
                process_zip_file(os.path.join(root, file), experiment_name)

print(f"Data has been written to {output_file_name}")
