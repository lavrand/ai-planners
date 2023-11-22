import os
import tarfile
import re
import csv
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for folder naming
FOLDER_PREFIX = "archive_pfile_"
METRICS = ["Time", "Discounted time", "Metareasoning time (not discounted)", "Dispatch metareasoning time (not discounted)", "Peak memory", "Nodes Generated", "Nodes Expanded", "Nodes Evaluated", "Nodes Tunneled", "Nodes memoised with open actions", "Nodes memoised without open actions", "Nodes pruned by memoisation"]

# Data structure to store values
data = {metric: {} for metric in METRICS}

def extract_tar_gz(tar_path, extract_path):
    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=extract_path)
            logging.info(f"Extracted {tar_path} into {extract_path}")
    except Exception as e:
        logging.error(f"Failed to extract {tar_path}: {e}")

def parse_metrics(file_path, file_identifier, disp_type):
    try:
        with open(file_path, "r") as file:
            for line in file:
                for metric in METRICS:
                    if metric in line:
                        value = float(re.findall(r"[-+]?\d*\.\d+|\d+", line)[0])
                        if file_identifier not in data[metric]:
                            data[metric][file_identifier] = {'disp': 'N/A', 'no-disp': 'N/A'}
                        data[metric][file_identifier][disp_type] = value
            logging.info(f"Processed metrics from {file_path}")
    except Exception as e:
        logging.error(f"Error parsing metrics from {file_path}: {e}")

def sort_identifiers(identifier):
    parts = identifier.split('-')
    return [int(parts[0]), int(parts[1])]

def main():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_path, "_nodes_analysis")
    os.makedirs(output_dir, exist_ok=True)

    for dir_name in os.listdir(base_path):
        if dir_name.startswith(FOLDER_PREFIX):
            dir_number = dir_name.split('_')[2]  # Extracting the first number (e.g., '25' from 'archive_pfile_25_13')
            full_path = os.path.join(base_path, dir_name)
            if os.path.isdir(full_path):
                logging.info(f"Processing directory {full_path}")
                for tar_file in os.listdir(full_path):
                    if tar_file.endswith(".tar.gz"):
                        extract_tar_gz(os.path.join(full_path, tar_file), full_path)

                        for disp_type in ["disp", "no-disp"]:
                            path = os.path.join(full_path, disp_type)
                            if os.path.isdir(path):
                                for file in os.listdir(path):
                                    if file.startswith(dir_number + "-"):
                                        file_path = os.path.join(path, file)
                                        file_identifier = f"{dir_number}-{file.split('-')[1]}"
                                        parse_metrics(file_path, file_identifier, disp_type)
            else:
                logging.warning(f"Directory {full_path} does not exist")

    # Generate CSV files
    for metric, values in data.items():
        sorted_values = sorted(values.items(), key=lambda x: sort_identifiers(x[0]))
        csv_file_path = os.path.join(output_dir, metric.replace(' ', '_') + '.csv')
        try:
            with open(csv_file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                header = ['Identifier', 'disp', 'no-disp']
                csvwriter.writerow(header)
                for identifier, disp_values in sorted_values:
                    row = [identifier, disp_values['disp'], disp_values['no-disp']]
                    csvwriter.writerow(row)
            logging.info(f"CSV file created: {csv_file_path}")
        except Exception as e:
            logging.error(f"Error writing to CSV file {csv_file_path}: {e}")

if __name__ == "__main__":
    main()
