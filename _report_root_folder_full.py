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
    csv_writer.writerow(["File", "disp", "nodisp"])


# Function to process tar.gz files
def process_tar_file(filepath):
    with tarfile.open(filepath, "r:gz") as archive:
        for member in archive.getmembers():  # Use getmembers to ensure it's iterable
            if member.isreg():  # Ensure it's a regular file, not a folder
                if member.name.endswith("times.csv"):
                    with archive.extractfile(member) as f:
                        file_content = f.read().decode("utf-8")
                        csv_reader = csv.reader(file_content.splitlines())
                        headers = next(csv_reader)  # Read the header row

                        # Validate headers if necessary
                        if headers[:3] == ["File", "disp", "nodisp"]:
                            for row in csv_reader:
                                # Extract data
                                file_name, disp, nodisp = row
                                with open(output_file_name, "a", newline='') as csvfile:
                                    csv_writer = csv.writer(csvfile)
                                    csv_writer.writerow([file_name, disp, nodisp])
                        else:
                            print(f"Unexpected columns in {member.name} within {filepath}")


# Start the traversal from specified directories
base_dirs = ["PC1", "PC2"]
for base in base_dirs:
    for root, dirs, files in os.walk(base):
        for file in files:
            match = re.match(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.tar\.gz$", file)
            if match:
                full_file_path = os.path.join(root, file)
                process_tar_file(full_file_path)

print(f"Data has been written to {output_file_name}")
