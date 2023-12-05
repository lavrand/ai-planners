import math

# Constants
TOTAL_INPUT = 300  # Total input value
N = 12              # Number of configuration files

# New constants to replace
TIME_BASED_ON_EXPANSIONS_PER_SECOND = 500
PLAN_SEARCH_TIMEOUT_SECONDS = 60
DOMAIN = "rcll_domain_production_durations_time_windows.pddl"
SUBTREE_FOCUS_THRESHOLD = 1
DISPATCH_THRESHOLD = 0.1 # was 0.025

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

    # Update the relevant lines
    with open(config_file_name, 'w') as file:
        for line in lines:
            if line.strip().startswith('PFILE_START ='):
                file.write(f"PFILE_START = {start}\n")
            elif line.strip().startswith('PFILE_END ='):
                file.write(f"PFILE_END = {end}\n")
            elif line.strip().startswith('time_based_on_expansions_per_second ='):
                file.write(f"time_based_on_expansions_per_second = {TIME_BASED_ON_EXPANSIONS_PER_SECOND}\n")
            elif line.strip().startswith('PLAN_SEARCH_TIMEOUT_SECONDS ='):
                file.write(f"PLAN_SEARCH_TIMEOUT_SECONDS = {PLAN_SEARCH_TIMEOUT_SECONDS}\n")
            elif line.strip().startswith('DOMAIN ='):
                file.write(f"DOMAIN = {DOMAIN}\n")
            elif line.strip().startswith('subtree_focus_threshold ='):
                file.write(f"subtree_focus_threshold = {SUBTREE_FOCUS_THRESHOLD}\n")
            elif line.strip().startswith('dispatch_threshold ='):
                file.write(f"dispatch_threshold = {DISPATCH_THRESHOLD}\n")
            else:
                file.write(line)

print("Configuration files have been updated.")
