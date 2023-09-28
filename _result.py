import os
import csv
import tarfile
import re

# Define the output file name
output_file_name = "output.csv"

# Write header to output file
with open(output_file_name, "w") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["experiment", "disp", "nodisp"])

# Loop through all files in the directory
for filename in os.listdir("."):
    match = re.match(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.tar\.gz$", filename)
    if match:
        experiment_name = match.group(1)

        # Extract timesDispBetter.csv from the tar.gz file
        with tarfile.open(filename, "r:gz") as archive:
            for member in archive:
                if member.name.endswith("timesDispBetter.csv"):
                    with archive.extractfile(member) as f:
                        file_content = f.read().decode("utf-8")
                        csv_reader = csv.reader(file_content.splitlines())
                        next(csv_reader)  # Skip header
                        for row in csv_reader:
                            disp, nodisp = row[1], row[2]
                            if disp != "9999" and nodisp != "99999":
                                with open(output_file_name, "a") as csvfile:
                                    csv_writer = csv.writer(csvfile)
                                    csv_writer.writerow([experiment_name, disp, nodisp])

print(f"Data has been written to {output_file_name}")
