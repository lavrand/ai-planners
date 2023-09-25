import subprocess
from datetime import datetime
import os
import re
import csv
import signal

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

# Function to run the dispscript commands
def run_dispscript():
    for i in range(1, 101):
        command = base_command_common + "--use-dispatcher LPFThreshold " + base_command_end + str(i) + " > disp/15-" + str(i)
        print(f"[{datetime.now()}] Running disp command for file 15-{i}...")
        run_subprocess(command, i)
        print(f"[{datetime.now()}] Finished disp command for file 15-{i}.")

# Function to run the nodispscript commands
def run_nodispscript():
    for i in range(78, 101):
        command = base_command_common + base_command_end + str(i) + " > nodisp/15-" + str(i)
        print(f"[{datetime.now()}] Running nodisp command for file 15-{i}...")
        run_subprocess(command, i)
        print(f"[{datetime.now()}] Finished nodisp command for file 15-{i}.")


def run_subprocess(command, i):
    stdout, stderr = None, None  # Initialize these to avoid UnboundLocalError

    # Start the process in a new session
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    try:
        # communicate() waits for the process to complete or for the timeout to expire
        stdout, stderr = process.communicate(timeout=60)
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
# run_dispscript()
# run_nodispscript()

# Extract time from the line
def extract_time(line):
    try:
        return float(line.split()[2])
    except:
        return "N/A"

# Extract execution time data and write to CSV
def extract_time_and_write_csv():
    with open(csv_filename, 'w', newline='') as csvfile, open(csv_filename_better, 'w', newline='') as csvbetterfile:
        csvwriter = csv.writer(csvfile)
        csvbetterwriter = csv.writer(csvbetterfile)
        csvwriter.writerow(['File', 'disp', 'nodisp'])
        csvbetterwriter.writerow(['File', 'disp', 'nodisp'])

        for i in range(1, 101):  # 1 to 100 inclusive
            filename = base_filename + str(i)
            times = [filename]  # Start with filename as first column

            disp_time = "N/A"
            nodisp_time = "N/A"

            for directory in directories:
                filepath = os.path.join(directory, filename)

                if os.path.exists(filepath):
                    with open(filepath, 'r') as f:
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
                            times.append("N/A")
                else:
                    times.append("N/A")

            # Write extracted times to CSV
            csvwriter.writerow(times)

            # If 'disp' is faster than 'nodisp', write to the better times file
            if isinstance(disp_time, float) and isinstance(nodisp_time, float) and disp_time < nodisp_time:
                csvbetterwriter.writerow(times)


# extract_time_and_write_csv('disp')
# extract_time_and_write_csv('nodisp')
extract_time_and_write_csv()

# Generate the timesDispBetter file
with open('disp.csv', 'r') as dispfile, open('nodisp.csv', 'r') as nodispfile, open('timesDispBetter.csv', 'w') as outfile:
    dispreader = csv.reader(dispfile)
    nodispreader = csv.reader(nodispfile)
    next(dispreader)  # skip headers
    next(nodispreader)  # skip headers
    for disp_row, nodisp_row in zip(dispreader, nodispreader):
        if float(disp_row[1]) < float(nodisp_row[1]):
            outfile.write(f"{disp_row[0]}: {disp_row[1]}s < {nodisp_row[1]}s\n")
