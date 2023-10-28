import subprocess
import tarfile
from datetime import datetime
import os
import re
import csv
import signal
import shutil
import multiprocessing
from functools import partial

from _execute_command import execute_command
from _execute_command_args import execute_command_args
from _replace_deadlines import replace_deadlines

# DOMAIN = 'driverlogTimed.pddl'
# AT = 'at'
# OBJECT = 'package'

DOMAIN = 'DepotsTime.pddl'
AT = 'on'
OBJECT = 'crate'

# DOMAIN = 'zenotravelTandN.pddl'
# AT = 'at'
# OBJECT = 'person'

# DOMAIN = 'CTRover.pddl'
# AT = 'at'
# OBJECT = 'rover'

PLAN_SEARCH_TIMEOUT_SECONDS = 60
EXPERIMENTS = 100

# Flag to determine whether to use specific PFILE_N values or a range
USE_SPECIFIC_PFILE_VALUES = True  # Set to False to use the PFILE_START to PFILE_END range

# Specific values for PFILE_N, used if USE_SPECIFIC_PFILE_VALUES is True
SPECIFIC_PFILE_VALUES = [7, 10]

# Define the range for PFILE_N
PFILE_START = 10
PFILE_N = PFILE_START
# PFILE_END = 22  # This allows the loop to go up to PFILE_N = 22 'DepotsTime.pddl'
PFILE_END = 10 # This allows the loop to go up to PFILE_N = 20 'driverlogTimed.pddl' 'zenotravelTandN.pddl'

PERTURB_RND = 0
PERTURB_MINUS = -50
PERTURB_PLUS = 50
__STEP = 5

MULTIPROCESSING_CPU_COUNT_MINUS = 2

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


# Main loop to run everything in an infinite cycle
while True:
    # Determine which PFILE_N values to use based on the flag
    if USE_SPECIFIC_PFILE_VALUES:
        pfile_values = SPECIFIC_PFILE_VALUES  # use the specific values
    else:
        pfile_values = range(PFILE_START, PFILE_END + 1)  # use the range

    for current_pfile in range(PFILE_START, PFILE_END + 1):  # Looping over the defined range
        try:  # Add a try block to catch any exceptions that occur for a single PFILE_N.
            PFILE_N = current_pfile  # Updating the PFILE_N value for this iteration
            PFILE = f"pfile{PFILE_N}"

            for current_perturb_minus in range(PERTURB_MINUS, PERTURB_PLUS + 1, __STEP):  # Iterating from -50 to 50 inclusive with step 10
                PERTURB_MINUS = current_perturb_minus  # Updating the PERTURB_MINUS value for this iteration

                print(f"[{datetime.now()}] Starting a new set of experiments for PFILE_N = {PFILE_N} with PERTURB_MINUS = {PERTURB_MINUS} ...")

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
                    ("./gen", [f'{PFILE_N}', f'{DOMAIN}', f'{AT}', f'{OBJECT}', f'{PERTURB_RND}', f'{PERTURB_MINUS}'])
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
                        # Execute the command with arguments, and wait for it to complete, but not longer than 120 seconds
                        result = subprocess.run(cmd, check=True, text=True, capture_output=True, timeout=120)

                        # If the command was successful, result.stdout will contain the output
                        print(result.stdout)

                    except subprocess.TimeoutExpired:
                        # Handle the timeout exception as you see fit
                        print("The command did not complete within 120 seconds.")
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

                base_command_common = ("./rewrite-no-lp --time-based-on-expansions-per-second 500 "
                                       "--include-metareasoning-time --multiply-TILs-by 1 "
                                       "--real-to-plan-time-multiplier 1 --calculate-Q-interval 100 "
                                       "--add-weighted-f-value-to-Q -0.000001 --min-probability-failure 0.001 "
                                       "--slack-from-heuristic --forbid-self-overlapping-actions "
                                       "--deadline-aware-open-list IJCAI --ijcai-gamma 1 --ijcai-t_u 100 "
                                       "--icaps-for-n-expansions 100 --time-aware-heuristic 1 "
                                       "--dispatch-frontier-size 10 --subtree-focus-threshold 0.025 "
                                       "--dispatch-threshold 0.025 --optimistic-lst-for-dispatch-reasoning ")

                base_command_end = (f" %s withdeadlines-ontime-pfile{PFILE_N}-" % DOMAIN)


                # Function to run the dispscript commands
                def run_dispscript(i):
                    command = base_command_common + "--use-dispatcher LPFThreshold " + base_command_end + str(
                        i) + f" > disp/{PFILE_N}-" + str(i)
                    print(f"[{datetime.now()}] Running disp command for file {PFILE_N}-{i}...")
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

                        for i in range(1, EXPERIMENTS + 1):  # 1 to 100 inclusive
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
