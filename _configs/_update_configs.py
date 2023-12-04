import math

# Constants
TOTAL_INPUT = 300  # Total input value
N = 12              # Number of configuration files

# Function to calculate the range for each file
def calculate_ranges(total_input, num_files):
    range_size = math.ceil(total_input / num_files)
    return [(i * range_size + 1, min((i + 1) * range_size, total_input)) for i in range(num_files)]

# Calculate ranges
ranges = calculate_ranges(TOTAL_INPUT, N)

# Update configuration files
for i, (start, end) in enumerate(ranges, 1):
    config_file_name = f"config{i}.ini"  # Assuming the files are named config1.txt, config2.txt, etc.

    # Read existing content
    with open(config_file_name, 'r') as file:
        lines = file.readlines()

    # Update PFILE_START and PFILE_END
    with open(config_file_name, 'w') as file:
        for line in lines:
            if line.strip().startswith('PFILE_START ='):
                file.write(f"PFILE_START = {start}\n")
            elif line.strip().startswith('PFILE_END ='):
                file.write(f"PFILE_END = {end}\n")
            else:
                file.write(line)

print("Configuration files have been updated.")
