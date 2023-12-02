import configparser
import itertools
import multiprocessing
import os
import signal
import subprocess
import sys
import tarfile
from datetime import datetime

from _replace_deadlines import replace_deadlines


# Define a logging function
def log_message(message, log_file):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}\n")

# Updated function for creating and organizing directories
def create_and_organize_directories(current_pfile_n):
    pfile_directory = f"p{current_pfile_n}"
    if not os.path.exists(pfile_directory):
        os.makedirs(pfile_directory)

    for dir_name in ['disp', 'nodisp']:
        dir_path = os.path.join(pfile_directory, dir_name)
        if os.path.exists(dir_path) and not os.path.isdir(dir_path):
            os.remove(dir_path)  # Remove if it exists and is not a directory
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

# Check if a command line argument has been provided
if len(sys.argv) < 2:
    log_message("Usage: python main.py <config_file>")
    sys.exit(1)

# The second command line argument is expected to be the config file name
config_file = sys.argv[1]

# Initialize the configparser
config = configparser.ConfigParser()

log_file_error = open("error_log.txt", 'a')

# Read the configuration file passed as a command line argument
try:
    config.read(config_file)
except configparser.DuplicateOptionError as e:
    log_message(f"Duplicate option error in config file: {e}", log_file_error)
    # Handle the exception (e.g., exit the script or ignore the duplicate)


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
deadline_on_first_snap_action = config.get('DEFAULT', 'deadline_on_first_snap_action')
ORIGINAL_PFILES = config.getboolean('DEFAULT', 'ORIGINAL_PFILES')
log_file_path = config.get('DEFAULT', 'log_file_path')
CPU_COUNT_PC = multiprocessing.cpu_count()
CPU_COUNT = CPU_COUNT_PC - MULTIPROCESSING_CPU_COUNT_MINUS

PFILE_N = PFILE_START


PFILE = f"pfile{PFILE_N}"
FOREST_DEADLINES_ENABLED = False  # DOUBLECHECK THIS IS DISABLED

# Flag to enable or disable parallel processing
ENABLE_PARALLEL = True

log_file = open(log_file_path, 'a')

# Updated archiving function
def create_archive(current_pfile_n):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    archive_name = f"{timestamp}_{current_pfile_n}.tar.gz"
    archive_dir = f"archive_pfile_{current_pfile_n}"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    archive_path = os.path.join(archive_dir, archive_name)
    pfile_directory = f"p{current_pfile_n}"
    items_to_archive = [os.path.join(pfile_directory, 'disp'), os.path.join(pfile_directory, 'nodisp')]
    with tarfile.open(archive_path, 'w:gz') as archive:
        for item in items_to_archive:
            if os.path.exists(item):
                archive.add(item, arcname=os.path.basename(item))
    log_message(f"Created archive: {archive_path}", log_file)


# Create an infinite iterator over the specific PFILE values
pfile_cycle = itertools.cycle(SPECIFIC_PFILE_VALUES) if USE_SPECIFIC_PFILE_VALUES else None


# Determine which PFILE_N values to use based on the flag
if USE_SPECIFIC_PFILE_VALUES:
    pfile_values = [next(pfile_cycle)]   # use the specific values
else:
    pfile_values = range(PFILE_START, PFILE_END + 1)  # use the range

for current_pfile in pfile_values:  # Looping over the defined range
    try:  # Add a try block to catch any exceptions that occur for a single PFILE_N.
        PFILE_N = current_pfile  # Updating the PFILE_N value for this iteration
        PFILE = f"pfile{PFILE_N}"

        # Create and organize directories for current pfile
        create_and_organize_directories(PFILE_N)

        for current_perturb_minus in range(PERTURB_MINUS, PERTURB_PLUS + 1, __STEP):  # Iterating from -PERTURB_MINUS to PERTURB_PLUS inclusive with step 10
            PERTURB_MINUS_CUR = current_perturb_minus  # Updating the PERTURB_MINUS value for this iteration

            # log_message(f" Starting a new set of experiments for PFILE_N = {PFILE_N} with current_perturb_minus = {current_perturb_minus} ...", log_file)
            log_message(
                f" Starting a new set of experiments for PFILE_N = {PFILE_N} ...",
                log_file)

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
                    log_message(result.stdout, log_file)

                except subprocess.TimeoutExpired:
                    # Handle the timeout exception as you see fit
                    log_message("The command did not complete within timeout seconds.", log_file)
                    # Here you might choose to try the command again, or perhaps record the timeout in a log file

                except subprocess.CalledProcessError as e:
                    # Handle the exception for a non-zero exit code if check=True
                    log_message(f"The command failed because: {e.stderr}", log_file)
                    # Here you can do additional handling of the error, like retrying the command or logging the error

                except Exception as e:
                    log_message(f"An error occurred: {str(e)}", log_file)
                    return None


            if not (DEADLINE_ON_FIRST_SNAP or ORIGINAL_PFILES):
                # Execute each command using the run_subprocess function
                for cmd, args in commands_to_run:
                    log_message(f"Executing command: {cmd} {' '.join(args)}", log_file)
                    run_subprocess_args(cmd, args)

            if FOREST_DEADLINES_ENABLED:
                replace_deadlines(PFILE_N)
                log_message(f"Deadlines replaced successfully with random forest model prediction deadlines..", log_file)

            log_message(f" Finished running the generation script.", log_file)

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

            base_command_deadline_on_first_snap = (f" --deadline-on-first-snap-action {deadline_on_first_snap_action} ")
            if DEADLINE_ON_FIRST_SNAP:
                base_command_common += base_command_deadline_on_first_snap
                base_command_end = (f" %s pfile{PFILE_N}" % DOMAIN)
            elif ORIGINAL_PFILES:
                base_command_end = (f" %s pfile{PFILE_N}" % DOMAIN)
            else:
                base_command_end = (f" %s withdeadlines-ontime-pfile{PFILE_N}-" % DOMAIN)


            # Function to run the dispscript commands
            def run_dispscript(i):
                if DEADLINE_ON_FIRST_SNAP or ORIGINAL_PFILES:
                    command = base_command_common + "--use-dispatcher LPFThreshold " + base_command_end + f" > p{PFILE_N}/disp/{PFILE_N}"
                    log_message(f" Running disp command for file {PFILE_N}. Command: {command}", log_file)
                    run_subprocess(command, i)
                    log_message(f" Finished disp command for file {PFILE_N}.", log_file)
                else:
                    command = base_command_common + "--use-dispatcher LPFThreshold " + base_command_end + str(
                        i) + f" > disp/{PFILE_N}-" + str(i)
                    log_message(f" Running disp command for file {PFILE_N}-{i}. Command: {command}", log_file)
                    run_subprocess(command, i)
                    log_message(f" Finished disp command for file {PFILE_N}-{i}.", log_file)


            def run_nodispscript(i):
                if DEADLINE_ON_FIRST_SNAP or ORIGINAL_PFILES:
                    command = base_command_common + base_command_end + f" > p{PFILE_N}/nodisp/{PFILE_N}"
                    log_message(f" Running nodisp command for file {PFILE_N}. Command: {command}", log_file)
                    run_subprocess(command, i)
                    log_message(f" Finished nodisp command for file {PFILE_N}.", log_file)
                else:
                    command = base_command_common + base_command_end + str(
                        i) + f" > nodisp/{PFILE_N}-" + str(i)
                    log_message(f" Running nodisp command for file {PFILE_N}-{i}. Command: {command}", log_file)
                    run_subprocess(command, i)
                    log_message(f" Finished nodisp command for file {PFILE_N}-{i}.", log_file)


            def run_subprocess(command, i=None):
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
                    if i is not None:
                        log_message(f"Command #{i} took longer than timeout seconds and was killed!", log_file)
                    else:
                        log_message(f"Command took longer than timeout seconds and was killed!", log_file)
                else:
                    if process.returncode != 0:
                        if i is not None:
                            log_message(f"Command #{i} failed!", log_file)
                        else:
                            log_message(f"Command failed!", log_file)
                    else:
                        if i is not None:
                            log_message(f"Command #{i} completed successfully!", log_file)
                        else:
                            log_message(f"Command completed successfully!", log_file)

                # Return stdout, stderr, and returncode
                return stdout, stderr, process.returncode

            # Non-parallel execution as fallback
            for i in range(1, EXPERIMENTS + 1):
                run_dispscript(i)
                run_nodispscript(i)


            log_message(f" Finished current set of experiments. Starting archiving...", log_file)

            # Call the modified function with the current PFILE_N
            create_archive(PFILE_N)

            log_message(f" Finished archiving.", log_file)


            log_message(f" All PFILE_N experiments completed for this cycle. Restarting...", log_file)

    except Exception as e:  # Catch any type of exception
        log_message(f" An error occurred during processing for PFILE_N = {PFILE_N}: {str(e)}", log_file)
        log_message("Continuing with the next PFILE_N...", log_file)
        # Optionally, log the exception e to a log file or database for later analysis
    finally:
        # If there's any cleanup that ALWAYS needs to happen, put it here.
        pass


log_file.close()
log_file_error.close()
