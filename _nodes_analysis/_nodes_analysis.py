import os
import tarfile
import re
import csv

N = 100

# Constants for folder naming
FOLDER_PREFIX = "archive_pfile_"
ARCHIVE_SUFFIXES = range(0, 100)  # Assuming the range of suffixes
METRICS = ["Time", "Discounted time", "Metareasoning time (not discounted)", "Dispatch metareasoning time (not discounted)", "Peak memory", "Nodes Generated", "Nodes Expanded", "Nodes Evaluated", "Nodes Tunneled", "Nodes memoised with open actions", "Nodes memoised without open actions", "Nodes pruned by memoisation"]

# Data structure to store values
data = {metric: {} for metric in METRICS}

def extract_tar_gz(tar_path, extract_path):
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=extract_path)

def parse_metrics(file_path, file_identifier, disp_type):
    with open(file_path, "r") as file:
        for line in file:
            for metric in METRICS:
                if metric in line:
                    value = float(re.findall(r"[-+]?\d*\.\d+|\d+", line)[0])
                    if file_identifier not in data[metric]:
                        data[metric][file_identifier] = {}
                    data[metric][file_identifier][disp_type] = value

def main():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for suffix in ARCHIVE_SUFFIXES:
        for n in range(1, N):
            dir_name = os.path.join(base_path, F"{FOLDER_PREFIX}{n}_{suffix}")
            if os.path.exists(dir_name):
                for tar_file in os.listdir(dir_name):
                    if tar_file.endswith(".tar.gz"):
                        extract_tar_gz(os.path.join(dir_name, tar_file), dir_name)

                        for disp_type in ["disp", "no-disp"]:
                            path = os.path.join(dir_name, disp_type)
                            if os.path.isdir(path):
                                for file in os.listdir(path):
                                    if file.startswith("{n}-"):
                                        file_path = os.path.join(path, file)
                                        file_identifier = f"{n}-{file.split('-')[1]}"
                                        parse_metrics(file_path, file_identifier, disp_type)

    # Generate CSV files
    for metric, values in data.items():
        with open(os.path.join(base_path, metric + '.csv'), 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            header = ['Identifier', 'disp', 'no-disp']
            csvwriter.writerow(header)
            for identifier, disp_values in values.items():
                row = [identifier, disp_values.get('disp', 'N/A'), disp_values.get('no-disp', 'N/A')]
                csvwriter.writerow(row)

if __name__ == "__main__":
    main()
