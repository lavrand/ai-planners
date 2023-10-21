import csv
import re

# Function to read the CSV file and get the replacement values
def get_replacement_values(csv_file):
    with open(csv_file, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # skip the header
        return [row[:-1] for row in csvreader]  # collect all columns except the last

# Function to replace values in a single file
def process_file(file_path, new_values):
    # Read in the file
    with open(file_path, 'r') as file:
        file_lines = file.readlines()

    # Pattern to identify the lines with deadlines
    deadline_pattern = re.compile(r'\(at (.+?) \(not \(still-on-time crate\d+\)\)\)')

    # Pattern to match numbers after 'at'
    number_pattern = re.compile(r'(?<=\(at )-?\d+\.?\d*')

    new_file_lines = []
    value_index = 0  # to keep track of which value to use

    for line in file_lines:
        if deadline_pattern.search(line):  # this line contains a deadline
            new_line = re.sub(number_pattern, new_values[value_index], line)  # replace the number
            value_index += 1  # move to the next value for the next match
            new_file_lines.append(new_line)
        else:
            new_file_lines.append(line)  # keep the line as is if no deadline is found

    # Write the file out again
    with open(file_path, 'w') as file:
        file.writelines(new_file_lines)

def replace_deadlines():
    csv_file = 'top_100_predicted_nodisp_disp.csv'
    replacement_values_list = get_replacement_values(csv_file)

    # Process each file with its corresponding replacement values
    for i, new_values in enumerate(replacement_values_list, start=1):
        file_name = f'withdeadlines-ontime-pfile7-{i}'
        try:
            process_file(file_name, new_values)
            print(f'Processed {file_name}')
        except Exception as e:
            print(f'Could not process {file_name}: {e}')

if __name__ == "__main__":
    replace_deadlines()
