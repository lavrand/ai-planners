import subprocess
import tarfile
from datetime import datetime
import os
import re
import csv
import signal
import shutil

PLAN_SEARCH_TIMEOUT_SECONDS = 1800


def create_archive():
    """Archives specified directories and files."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    archive_name = f"{timestamp}.tar.gz"

    # List of directories and files to archive
    items_to_archive = ['disp', 'nodisp', 'times.csv', 'timesDispBetter.csv']

    # Adding files withdeadlines-ontime-pfile15-1 to withdeadlines-ontime-pfile15-100
    items_to_archive.extend([f"withdeadlines-ontime-pfile15-{i}" for i in range(1, 101)])

    # Create the archive
    with tarfile.open(archive_name, 'w:gz') as archive:
        for item in items_to_archive:
            if os.path.exists(item):  # Check if the item exists before adding
                archive.add(item)

    print(f"[{datetime.now()}] Created archive: {archive_name}")


def remove_folders_and_files():
    """Deletes the specified directories and files."""
    items_to_delete = ['disp', 'nodisp', 'times.csv', 'timesDispBetter.csv']

    # Adding files withdeadlines-ontime-pfile15-1 to withdeadlines-ontime-pfile15-100
    items_to_delete.extend([f"withdeadlines-ontime-pfile15-{i}" for i in range(1, 101)])

    for item in items_to_delete:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)

    print(f"[{datetime.now()}] Removed specified folders and files.")


__EXPERIMENTS = 100

# Main loop to run everything in an infinite cycle
while True:
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
    base_filename = "15-"

    base_command_common = ("./rewrite-no-lp --time-based-on-expansions-per-second 500 "
                           "--include-metareasoning-time --multiply-TILs-by 1 "
                           "--real-to-plan-time-multiplier 1 --calculate-Q-interval 100 "
                           "--add-weighted-f-value-to-Q -0.000001 --min-probability-failure 0.001 "
                           "--slack-from-heuristic --forbid-self-overlapping-actions "
                           "--deadline-aware-open-list IJCAI --ijcai-gamma 1 --ijcai-t_u 100 "
                           "--icaps-for-n-expansions 100 --time-aware-heuristic 1 "
                           "--dispatch-frontier-size 10 --subtree-focus-threshold 0.025 "
                           "--dispatch-threshold 0.025 --optimistic-lst-for-dispatch-reasoning ")

    base_command_end = (" driverlogTimed.pddl withdeadlines-ontime-pfile15-")


    def invoke_gen_script():
        # The command to invoke the generic script
        gen_script_command = "./gen"

        print(f"[{datetime.now()}] Running the generation script...")

        result = subprocess.run(gen_script_command, shell=True, check=True)

        if result.returncode != 0:
            print(f"Error running the generation script! Exiting.")
            exit(1)

        print(f"[{datetime.now()}] Finished running the generation script.")


    invoke_gen_script()


    # Function to run the dispscript commands
    def run_dispscript():
        for i in range(1, __EXPERIMENTS + 1):
            command = base_command_common + "--use-dispatcher LPFThreshold " + base_command_end + str(
                i) + " > disp/15-" + str(i)
            print(f"[{datetime.now()}] Running disp command for file 15-{i}...")
            run_subprocess(command, i)
            print(f"[{datetime.now()}] Finished disp command for file 15-{i}.")


    # Function to run the nodispscript commands
    def run_nodispscript():
        for i in range(1, __EXPERIMENTS + 1):
            command = base_command_common + base_command_end + str(i) + " > nodisp/15-" + str(i)
            print(f"[{datetime.now()}] Running nodisp command for file 15-{i}...")
            run_subprocess(command, i)
            print(f"[{datetime.now()}] Finished nodisp command for file 15-{i}.")


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
            print(f"Command #{i} took longer than 60 seconds and was killed!")
        else:
            if process.returncode != 0:
                print(f"Command #{i} failed!")
            else:
                print(f"Command #{i} completed successfully!")

        # Return stdout, stderr, and returncode
        return stdout, stderr, process.returncode


    # Execute the scripts
    run_dispscript()
    run_nodispscript()


    # Extract time from the line
    def extract_time(line):
        try:
            return float(line.split()[2])
        except:
            return "8888"


    # Extract execution time data and write to CSV
    def extract_time_and_write_csv():
        with open(csv_filename, 'w', newline='') as csvfile, open(csv_filename_better, 'w',
                                                                  newline='') as csvbetterfile:
            csvwriter = csv.writer(csvfile)
            csvbetterwriter = csv.writer(csvbetterfile)
            csvwriter.writerow(['File', 'disp', 'nodisp'])
            csvbetterwriter.writerow(['File', 'disp', 'nodisp'])

            for i in range(1, __EXPERIMENTS + 1):  # 1 to 100 inclusive
                filename = base_filename + str(i)
                times = [filename]  # Start with filename as first column

                disp_time = 99
                nodisp_time = 99

                for directory in directories:
                    filepath = os.path.join(directory, filename)

                    if os.path.exists(filepath):
                        with open(filepath, 'r') as f:

                            # ;;;; Problem Unsolvable
                            line_unsolvable = next(
                                (l for l in f.readlines() if l.startswith(";;;; Problem Unsolvable")), None)
                            if not line_unsolvable:
                                # Read the file lines and filter for the line with '; Time'
                                line = next((l for l in f.readlines() if l.startswith("; Time")), None)

                                if line:
                                    time_val = extract_time(line)
                                    if directory == 'disp':
                                        disp_time = time_val
                                    else:
                                        nodisp_time = time_val
                                    times.append(time_val)
                                else:
                                    times.append(999)
                            else:
                                times.append(9999)
                    else:
                        times.append(99999)

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
        rows = [row for row in reader if int(row[1]) < int(row[2])]

    # Write the filtered rows to timesDispBetter.csv
    with open('timesDispBetter.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"[{datetime.now()}] Finished current set of experiments. Starting archiving...")

    # Once the script finishes its run
    create_archive()
    print(f"[{datetime.now()}] Finished archiving.")

    print(f"[{datetime.now()}] Starting removing cache folder and files.")
    remove_folders_and_files()
    print(f"[{datetime.now()}] Finished removing cache folder and files.")
