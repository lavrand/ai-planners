import os
import tarfile
import re
import csv
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
FOLDER_PREFIX = "archive_pfile_"
METRICS = ["Time", "Discounted time", "Metareasoning time (not discounted)", "Dispatch metareasoning time (not discounted)", "Peak memory", "Nodes Generated", "Nodes Expanded", "Nodes Evaluated", "Nodes Tunneled", "Nodes memoised with open actions", "Nodes memoised without open actions", "Nodes pruned by memoisation"]

# Data structures
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
            solution_status = "Not Determined"
            for line in file:
                for metric in METRICS:
                    if metric in line:
                        value = float(re.findall(r"[-+]?\d*\.\d+|\d+", line)[0])
                        if file_identifier not in data[metric]:
                            data[metric][file_identifier] = {'disp': 'N/A', 'nodisp': 'N/A'}
                        data[metric][file_identifier][disp_type] = value
                if ";;;; Solution Found" in line:
                    solution_status = "Solution Found"
                elif ";;;; Problem Unsolvable" in line:
                    solution_status = "Problem Unsolvable"

            if file_identifier not in solution_data:
                solution_data[file_identifier] = {'disp': 'Not Determined', 'nodisp': 'Not Determined'}
            solution_data[file_identifier][disp_type] = solution_status
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

                        # Iterate over 'disp' and 'nodisp' directories
                        for disp_type in ["disp", "nodisp"]:
                            disp_path = os.path.join(full_path, disp_type)
                            if os.path.isdir(disp_path):
                                for file in os.listdir(disp_path):
                                    if file.startswith(dir_number + "-"):
                                        file_path = os.path.join(disp_path, file)
                                        file_identifier = f"{dir_number}-{file.split('-')[1]}"
                                        parse_metrics(file_path, file_identifier, disp_type)

    # Generate Solution.csv file
    solution_csv_path = os.path.join(output_dir, 'Solution.csv')
    try:
        with open(solution_csv_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            header = ['Identifier', 'disp', 'nodisp']
            csvwriter.writerow(header)

            # Sort the solution data before writing to CSV
            sorted_solution_data = sorted(solution_data.items(), key=lambda x: sort_identifiers(x[0]))
            for identifier, status in sorted_solution_data:
                csvwriter.writerow([identifier, status['disp'], status['nodisp']])

        logging.info(f"CSV file created: {solution_csv_path}")
    except Exception as e:
        logging.error(f"Error writing to CSV file {solution_csv_path}: {e}")

if __name__ == "__main__":
    main()