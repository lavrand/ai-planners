import subprocess
import tarfile
from datetime import datetime
import os
import re
import csv
import signal
import shutil
import multiprocessing
import itertools
from functools import partial
from _execute_command import execute_command
from _execute_command_args import execute_command_args
from _replace_deadlines import replace_deadlines
import configparser
import sys

# Check if a command line argument has been provided
if len(sys.argv) < 2:
    print("Usage: python main.py <config_file>")
    sys.exit(1)

# The second command line argument is expected to be the config file name
config_file = sys.argv[1]

# Initialize the configparser
config = configparser.ConfigParser()

# Read the configuration file passed as a command line argument
config.read(config_file)

# Retrieve the values from the config file
DOMAIN = config.get('DEFAULT', 'DOMAIN')
AT = config.get('DEFAULT', 'AT')
OBJECT = config.get('DEFAULT', 'OBJECT')
PLAN_SEARCH_TIMEOUT_SECONDS = config.getint('DEFAULT', 'PLAN_SEARCH_TIMEOUT_SECONDS')
EXPERIMENTS = config.getint('DEFAULT', 'EXPERIMENTS')
USE_SPECIFIC_PFILE_VALUES = config.getboolean('DEFAULT', 'USE_SPECIFIC_PFILE_VALUES')

# For list of values, such as SPECIFIC_PFILE_VALUES, convert from comma-separated string to list of ints
SPECIFIC_PFILE_VALUES = [int(x.strip()) for x in config.get('DEFAULT', 'SPECIFIC_PFILE_VALUES').split(',')]

PFILE_START = config.getint('DEFAULT', 'PFILE_START')
PFILE_END = config.getint('DEFAULT', 'PFILE_END')
# PERTURB in %
PERTURB_RND = config.getint('DEFAULT', 'PERTURB_RND')
PERTURB_MINUS = config.getint('DEFAULT', 'PERTURB_MINUS')
PERTURB_PLUS = config.getint('DEFAULT', 'PERTURB_PLUS')
__STEP = config.getint('DEFAULT', '__STEP')
MULTIPROCESSING_CPU_COUNT_MINUS = config.getint('DEFAULT', 'MULTIPROCESSING_CPU_COUNT_MINUS')

time_based_on_expansions_per_second = config.getint('DEFAULT', 'time_based_on_expansions_per_second')
multiply_TILs_by = config.getint('DEFAULT', 'multiply_TILs_by')
real_to_plan_time_multiplier = config.getint('DEFAULT', 'real_to_plan_time_multiplier')
calculate_Q_interval = config.getint('DEFAULT', 'calculate_Q_interval')
add_weighted_f_value_to_Q = config.get('DEFAULT', 'add_weighted_f_value_to_Q')
min_probability_failure = config.get('DEFAULT', 'min_probability_failure')
deadline_aware_open_list = config.get('DEFAULT', 'deadline_aware_open_list')
ijcai_gamma = config.get('DEFAULT', 'ijcai_gamma')
ijcai_t_u = config.getint('DEFAULT', 'ijcai_t_u')
icaps_for_n_expansions = config.getint('DEFAULT', 'icaps_for_n_expansions')
time_aware_heuristic = config.getint('DEFAULT', 'time_aware_heuristic')
dispatch_frontier_size = config.getint('DEFAULT', 'dispatch_frontier_size')
subtree_focus_threshold = config.get('DEFAULT', 'subtree_focus_threshold')
dispatch_threshold = config.get('DEFAULT', 'dispatch_threshold')
RUN_ONCE = config.getboolean('DEFAULT', 'RUN_ONCE')
DEADLINE_ON_FIRST_SNAP = config.getboolean('DEFAULT', 'DEADLINE_ON_FIRST_SNAP')

PFILE_N = PFILE_START


PFILE = f"pfile{PFILE_N}"
FOREST_DEADLINES_ENABLED = False  # DOUBLECHECK THIS IS DISABLED

# Flag to enable or disable parallel processing
ENABLE_PARALLEL = True

def create_archive(current_pfile_n, pertrub_minus):
    """Archives specified directories and files into a folder specific to the current PFILE_N."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    archive_name = f"{timestamp}.tar.gz"

    # Define the directory based on the current PFILE_N
    archive_dir = f"archive_pfile_{current_pfile_n}_{pertrub_minus}"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)  # Create directory if it doesn't exist

    # Full path for the archive file
    archive_path = os.path.join(archive_dir, archive_name)

    # List of directories and files to archive
    items_to_archive = ['disp', 'nodisp', 'times.csv', 'timesDispBetter.csv']
    items_to_archive.extend([f"withdeadlines-ontime-pfile{current_pfile_n}-{i}" for i in range(1, 101)])

    # Create the archive
    with tarfile.open(archive_path, 'w:gz') as archive:
        for item in items_to_archive:
            if os.path.exists(item):  # Check if the item exists before adding
                archive.add(item)

    print(f"[{datetime.now()}] Created archive: {archive_path}")


def remove_folders_and_files():
    """Deletes the specified directories and files."""
    items_to_delete = ['disp', 'nodisp', 'times.csv', 'timesDispBetter.csv']

    items_to_delete.extend([f"withdeadlines-ontime-pfile{PFILE_N}-{i}" for i in range(1, 101)])

    for item in items_to_delete:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)

    print(f"[{datetime.now()}] Removed specified folders and files.")


# Create an infinite iterator over the specific PFILE values
pfile_cycle = itertools.cycle(SPECIFIC_PFILE_VALUES) if USE_SPECIFIC_PFILE_VALUES else None


# Main loop to run everything in an infinite cycle
while True:

    # Determine which PFILE_N values to use based on the flag
    if USE_SPECIFIC_PFILE_VALUES:
        pfile_values = [next(pfile_cycle)]   # use the specific values
    else:
        pfile_values = range(PFILE_START, PFILE_END + 1)  # use the range

    for current_pfile in pfile_values:  # Looping over the defined range
        try:  # Add a try block to catch any exceptions that occur for a single PFILE_N.
            PFILE_N = current_pfile  # Updating the PFILE_N value for this iteration
            PFILE = f"pfile{PFILE_N}"

            for current_perturb_minus in range(PERTURB_MINUS, PERTURB_PLUS + 1, __STEP):  # Iterating from -PERTURB_MINUS to PERTURB_PLUS inclusive with step 10
                PERTURB_MINUS_CUR = current_perturb_minus  # Updating the PERTURB_MINUS value for this iteration

                print(f"[{datetime.now()}] Starting a new set of experiments for PFILE_N = {PFILE_N} with current_perturb_minus = {current_perturb_minus} ...")

                print(f"[{datetime.now()}] Starting a new set of experiments...")
                # Create directories and set permissions
                for dir_name in ['disp', 'nodisp']:
                    if not os.path.exists(dir_name):
                        os.makedirs(dir_name)
                        os.chmod(dir_name, 0o755)

                # Directories to parse
                directories = ['disp', 'nodisp']

                # Output CSV filenames
                csv_filename = "times.csv"
                csv_filename_better = "timesDispBetter.csv"

                # Base filename pattern
                base_filename = f"{PFILE_N}-"

                # Define commands and arguments
                commands_to_run = [
                    ("./add_initially_on_time", [f'{PFILE}', f'{AT}', f'{OBJECT}']),
                    ("./run-planner-to-get-initial-plan", [f'{DOMAIN}', f"ontime-pfile{PFILE_N}"]),
                    ("./gen", [f'{PFILE_N}', f'{DOMAIN}', f'{AT}', f'{OBJECT}', f'{PERTURB_RND}', f'{PERTURB_MINUS_CUR}', f'{EXPERIMENTS}', f'{PLAN_SEARCH_TIMEOUT_SECONDS}', f'{subtree_focus_threshold}', f'{dispatch_threshold}']),
                    ("./run-planner-to-get-initial-plan", [f'{DOMAIN}', f"withdeadlines-ontime-pfile{PFILE_N}"])
                ]

                def run_subprocess_args(command, args):
                    """
                    Run a command with arguments and handle exceptions.

                    Parameters:
                    command (str): The command to execute.
                    args (list): A list of arguments for the command.
                    """
                    # Combine the command and its arguments into one list.
                    cmd = [command] + args

                    try:
                        # Execute the command with arguments, and wait for it to complete, but not longer than PLAN_SEARCH_TIMEOUT_SECONDS * 2
                        result = subprocess.run(cmd, check=True, text=True, capture_output=True, timeout=PLAN_SEARCH_TIMEOUT_SECONDS * 2)

                        # If the command was successful, result.stdout will contain the output
                        print(result.stdout)

                    except subprocess.TimeoutExpired:
                        # Handle the timeout exception as you see fit
                        print("The command did not complete within timeout seconds.")
                        # Here you might choose to try the command again, or perhaps record the timeout in a log file

                    except subprocess.CalledProcessError as e:
                        # Handle the exception for a non-zero exit code if check=True
                        print(f"The command failed because: {e.stderr}")
                        # Here you can do additional handling of the error, like retrying the command or logging the error

                    except Exception as e:
                        print(f"An error occurred: {str(e)}")
                        return None

                # Execute each command using the run_subprocess function
                for cmd, args in commands_to_run:
                    print(f"Executing command: {cmd} {' '.join(args)}")
                    run_subprocess_args(cmd, args)

                if FOREST_DEADLINES_ENABLED:
                    replace_deadlines(PFILE_N)
                    print(f"Deadlines replaced successfully with random forest model prediction deadlines..")

                print(f"[{datetime.now()}] Finished running the generation script.")

                base_command_common = (
                    f"./rewrite-no-lp --time-based-on-expansions-per-second {time_based_on_expansions_per_second} "
                    f"--include-metareasoning-time --multiply-TILs-by {multiply_TILs_by} "
                    f"--real-to-plan-time-multiplier {real_to_plan_time_multiplier} --calculate-Q-interval {calculate_Q_interval} "
                    f"--add-weighted-f-value-to-Q {add_weighted_f_value_to_Q} --min-probability-failure {min_probability_failure} "
                    f"--slack-from-heuristic --forbid-self-overlapping-actions "
                    f"--deadline-aware-open-list {deadline_aware_open_list} --ijcai-gamma {ijcai_gamma} --ijcai-t_u {ijcai_t_u} "
                    f"--icaps-for-n-expansions {icaps_for_n_expansions} --time-aware-heuristic {time_aware_heuristic} "
                    f"--dispatch-frontier-size {dispatch_frontier_size} --subtree-focus-threshold {subtree_focus_threshold} "
                    f"--dispatch-threshold {dispatch_threshold} --optimistic-lst-for-dispatch-reasoning "
                )

                base_command_deadline_on_first_snap = (f" --deadline-on-first-snap-action 0.5 ")
                if DEADLINE_ON_FIRST_SNAP:
                    base_command_common += base_command_deadline_on_first_snap
                base_command_end = (f" %s withdeadlines-ontime-pfile{PFILE_N}-" % DOMAIN)


                # Function to run the dispscript commands
                def run_dispscript(i):
                    command = base_command_common + "--use-dispatcher LPFThreshold " + base_command_end + str(
                        i) + f" > disp/{PFILE_N}-" + str(i)
                    print(f"[{datetime.now()}] Running disp command for file {PFILE_N}-{i}. Command: {command}")
                    run_subprocess(command, i)
                    print(f"[{datetime.now()}] Finished disp command for file {PFILE_N}-{i}.")


                def run_nodispscript(i):
                    command = base_command_common + base_command_end + str(i) + f" > nodisp/{PFILE_N}-" + str(i)
                    print(f"[{datetime.now()}] Running nodisp command for file {PFILE_N}-{i}...")
                    run_subprocess(command, i)
                    print(f"[{datetime.now()}] Finished nodisp command for file {PFILE_N}-{i}.")



                def run_subprocess(command, i):
                    stdout, stderr = None, None  # Initialize these to avoid UnboundLocalError

                    # Start the process in a new session
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               preexec_fn=os.setsid)
                    try:
                        # communicate() waits for the process to complete or for the timeout to expire
                        stdout, stderr = process.communicate(timeout=PLAN_SEARCH_TIMEOUT_SECONDS)
                    except subprocess.TimeoutExpired:
                        # If the timeout expires, kill the entire process group
                        os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # try to terminate the process group gracefully
                        process.wait(timeout=10)  # give it 10 seconds to terminate gracefully
                        if process.poll() is None:  # if the process is still running after 10 seconds
                            os.killpg(os.getpgid(process.pid), signal.SIGKILL)  # forcibly kill the process group
                        print(f"Command #{i} took longer than timeout seconds and was killed!")
                    else:
                        if process.returncode != 0:
                            print(f"Command #{i} failed!")
                        else:
                            print(f"Command #{i} completed successfully!")

                    # Return stdout, stderr, and returncode
                    return stdout, stderr, process.returncode

                # Define the number of processes to spawn. Ideally, this is the number of cores available.
                num_processes = multiprocessing.cpu_count() - MULTIPROCESSING_CPU_COUNT_MINUS if ENABLE_PARALLEL else 1
                # Log the number of processes
                print(f"[{datetime.now()}] Running with {num_processes} parallel processes.")

                # Execute the scripts
                if ENABLE_PARALLEL:
                    with multiprocessing.Pool(processes=num_processes) as pool:
                        pool.map(run_dispscript, range(1, EXPERIMENTS + 1))  # This will distribute the list of indexes to the available processes
                        pool.map(run_nodispscript, range(1, EXPERIMENTS + 1))
                else:
                    # Non-parallel execution as fallback
                    for i in range(1, EXPERIMENTS + 1):
                        run_dispscript(i)
                        run_nodispscript(i)

                # Extract time from the line
                def extract_time(line):
                    try:
                        return float(line.split()[2])
                    except:
                        # parsing code error
                        return "9999999"


                # Extract execution time data and write to CSV
                def extract_time_and_write_csv():
                    with open(csv_filename, 'w', newline='') as csvfile, open(csv_filename_better, 'w',
                                                                              newline='') as csvbetterfile:
                        csvwriter = csv.writer(csvfile)
                        csvbetterwriter = csv.writer(csvbetterfile)
                        csvwriter.writerow(['File', 'disp', 'nodisp'])
                        csvbetterwriter.writerow(['File', 'disp', 'nodisp'])

                        for i in range(1, EXPERIMENTS + 1):  # 1 to EXPERIMENTS inclusive
                            filename = base_filename + str(i)
                            times = [filename]  # Start with filename as first column

                            disp_time = 0
                            nodisp_time = 0

                            for directory in directories:
                                filepath = os.path.join(directory, filename)

                                if os.path.exists(filepath):
                                    with open(filepath, 'r') as f:

                                        lines = f.readlines()

                                        # ;;;; Problem Unsolvable
                                        line_unsolvable = next((l for l in lines if l.startswith(";;;; Problem Unsolvable")), None)
                                        if not line_unsolvable:
                                            # Search in the stored lines for the line with '; Time'
                                            line = next((l for l in lines if l.startswith("; Time")), None)

                                            if line:
                                                time_val = extract_time(line)
                                                if directory == 'disp':
                                                    disp_time = time_val
                                                else:
                                                    nodisp_time = time_val
                                                times.append(time_val)
                                            else:
                                                # no line for time code
                                                times.append(9999)
                                        else:
                                            # unsolvable code
                                            times.append(99999)
                                else:
                                    # filepath doesn't exist code
                                    times.append(999999)

                            # Write extracted times to CSV
                            csvwriter.writerow(times)

                            # If 'disp' is faster than 'nodisp', write to the better times file
                            if isinstance(disp_time, float) and isinstance(nodisp_time, float) and disp_time < nodisp_time:
                                csvbetterwriter.writerow(times)


                extract_time_and_write_csv()

                # Read the times.csv file
                with open('times.csv', 'r') as file:
                    reader = csv.reader(file)

                    # Extract headers and rows
                    headers = next(reader)
                    rows = [row for row in reader if float(row[1]) < float(row[2])]

                # Write the filtered rows to timesDispBetter.csv
                with open('timesDispBetter.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(rows)

                print(f"[{datetime.now()}] Finished current set of experiments. Starting archiving...")

                # Call the modified function with the current PFILE_N
                create_archive(PFILE_N, current_perturb_minus)

                print(f"[{datetime.now()}] Finished archiving.")

                print(f"[{datetime.now()}] Starting removing cache folder and files.")
                remove_folders_and_files()
                print(f"[{datetime.now()}] Finished removing cache folder and files.")

                print(f"[{datetime.now()}] All PFILE_N experiments completed for this cycle. Restarting...")

        except Exception as e:  # Catch any type of exception
            print(f"[{datetime.now()}] An error occurred during processing for PFILE_N = {PFILE_N}: {str(e)}")
            print("Continuing with the next PFILE_N...")
            # Optionally, log the exception e to a log file or database for later analysis
        finally:
            # If there's any cleanup that ALWAYS needs to happen, put it here.

            pass

    # Check if the loop should run only once
    if RUN_ONCE:
        break