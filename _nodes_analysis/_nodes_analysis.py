#!/usr/bin/python3
import os
import tarfile
import re
import csv
import logging

# Configure logging to file and console
log_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_nodes_analysis', 'nodes_analysis.log')
os.makedirs(os.path.dirname(log_filename), exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(log_filename)
console_handler = logging.StreamHandler()

logging.getLogger().addHandler(file_handler)
logging.getLogger().addHandler(console_handler)

# Constants for folder naming
FOLDER_PREFIX = "archive_pfile_"
METRICS = ["Time", "Discounted time", "Metareasoning time (not discounted)", "Dispatch metareasoning time (not discounted)", "Peak memory", "Nodes Generated", "Nodes Expanded", "Nodes Evaluated", "Nodes Tunneled", "Nodes memoised with open actions", "Nodes memoised without open actions", "Nodes pruned by memoisation"]

# Data structure to store values
data = {metric: {} for metric in METRICS}
solution_data = {}

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
            found = False
            for line in file:
                for metric in METRICS:
                    if metric in line:
                        found = True
                        value = float(re.findall(r"[-+]?\d*\.\d+|\d+", line)[0])
                        if file_identifier not in data[metric]:
                            data[metric][file_identifier] = {'disp': 'N/A', 'nodisp': 'N/A'}
                        data[metric][file_identifier][disp_type] = value
            if not found:
                logging.warning(f"Metrics not found in {file_path}")
                for metric in METRICS:
                    if file_identifier not in data[metric]:
                        data[metric][file_identifier] = {'disp': 'N/A', 'nodisp': 'N/A'}
                    data[metric][file_identifier][disp_type] = 'N/A'
            else:
                logging.info(f"Processed metrics from {file_path}")
    except Exception as e:
        logging.error(f"Error parsing metrics from {file_path}: {e}")


def sort_identifiers(identifier):
    return int(identifier)

def main():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_path, "_nodes_analysis")
    os.makedirs(output_dir, exist_ok=True)

    processed_identifiers = set()
    expected_identifiers = set()

    for dir_name in os.listdir(base_path):
        if dir_name.startswith(FOLDER_PREFIX):
            dir_number = dir_name.split('_')[2]
            expected_identifiers.add(dir_number)
            full_path = os.path.join(base_path, dir_name)
            if os.path.isdir(full_path):
                logging.info(f"Processing directory {full_path}")
                for tar_file in os.listdir(full_path):
                    if tar_file.endswith(".tar.gz"):
                        extract_tar_gz(os.path.join(full_path, tar_file), full_path)

                        for disp_type in ["disp", "nodisp"]:
                            path = os.path.join(full_path, disp_type)
                            if os.path.isdir(path):
                                for file in os.listdir(path):
                                    file_path = os.path.join(path, file)
                                    file_identifier = f"{dir_number}"
                                    parse_metrics(file_path, file_identifier, disp_type)
                                    processed_identifiers.add(file_identifier)

                                    # Determine solution status
                                    solution_status = "Not Determined"
                                    with open(file_path, "r") as file:
                                        for line in file:
                                            if ";;;; Solution Found" in line:
                                                solution_status = "Solution Found"
                                            elif ";;;; Problem Unsolvable" in line:
                                                solution_status = "Problem Unsolvable"
                                    if file_identifier not in solution_data:
                                        solution_data[file_identifier] = {'disp': 'Not Determined', 'nodisp': 'Not Determined'}
                                    solution_data[file_identifier][disp_type] = solution_status
            else:
                logging.warning(f"Directory {full_path} does not exist")

    for metric, values in data.items():
        sorted_values = sorted(values.items(), key=lambda x: sort_identifiers(x[0]))
        csv_file_path = os.path.join(output_dir, metric.replace(' ', '_') + '.csv')
        try:
            with open(csv_file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                header = ['Identifier', 'disp', 'nodisp']
                csvwriter.writerow(header)
                for identifier, disp_values in sorted_values:
                    row = [identifier, disp_values['disp'], disp_values['nodisp']]
                    csvwriter.writerow(row)
            logging.info(f"CSV file created: {csv_file_path}")
        except Exception as e:
            logging.error(f"Error writing to CSV file {csv_file_path}: {e}")

    missed_identifiers = expected_identifiers - processed_identifiers
    if missed_identifiers:
        logging.warning(f"Missed processing the following identifiers: {missed_identifiers}")

    # Generate and sort Solution.csv file
    sorted_solution_data = sorted(solution_data.items(), key=lambda x: sort_identifiers(x[0]))
    solution_csv_path = os.path.join(output_dir, 'Solution.csv')
    try:
        with open(solution_csv_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            header = ['Identifier', 'disp', 'nodisp']
            csvwriter.writerow(header)
            for identifier, disp_values in sorted_solution_data:
                row = [identifier, disp_values['disp'], disp_values['nodisp']]
                csvwriter.writerow(row)
        logging.info(f"CSV file created: {solution_csv_path}")
    except Exception as e:
        logging.error(f"Error writing to CSV file {solution_csv_path}: {e}")

if __name__ == "__main__":
    main()
