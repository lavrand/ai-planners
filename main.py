import subprocess
from datetime import datetime
import os
import re
import csv

# Create directories and set permissions
for dir_name in ['disp', 'nodisp']:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        os.chmod(dir_name, 0o755)

base_command_common = ("./rewrite-no-lp --time-based-on-expansions-per-second 500 "
                       "--include-metareasoning-time --multiply-TILs-by 1 "
                       "--real-to-plan-time-multiplier 1 --calculate-Q-interval 100 "
                       "--add-weighted-f-value-to-Q -0.000001 --min-probability-failure 0.001 "
                       "--slack-from-heuristic --forbid-self-overlapping-actions "
                       "--deadline-aware-open-list IJCAI --ijcai-gamma 1 --ijcai-t_u 100 "
                       "--icaps-for-n-expansions 100 --time-aware-heuristic 1 "
                       "--dispatch-frontier-size 10 --subtree-focus-threshold 0.025 "
                       "--dispatch-threshold 0.025 --optimistic-lst-for-dispatch-reasoning driverlogTimed.pddl withdeadlines-ontime-pfile15-")

# Function to run the dispscript commands
def run_dispscript():
    for i in range(1, 101):
        command = base_command_common + "--use-dispatcher LPFThreshold " + str(i) + " > disp/15-" + str(i)
        print(f"[{datetime.now()}] Running disp command for file 15-{i}...")
        subprocess.run(command, shell=True, check=True)
        print(f"[{datetime.now()}] Finished disp command for file 15-{i}.")

# Function to run the nodispscript commands
def run_nodispscript():
    for i in range(1, 101):
        command = base_command_common + str(i) + " > nodisp/15-" + str(i)
        print(f"[{datetime.now()}] Running nodisp command for file 15-{i}...")
        subprocess.run(command, shell=True, check=True)
        print(f"[{datetime.now()}] Finished nodisp command for file 15-{i}.")

# Execute the scripts
run_dispscript()
run_nodispscript()

# Extract execution time data and write to CSV
def extract_time_and_write_csv(folder_name):
    regex_pattern = re.compile(r"Total time: ([\d.]+)s|Killed|Time limit exceeded")
    with open(f"{folder_name}.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["File", "Time (s)"])
        for i in range(1, 101):
            file_path = f"{folder_name}/15-{i}"
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    matches = regex_pattern.findall(content)
                    if matches:
                        match = matches[0]
                        time_value = match[0] if match[0] else "60"
                        csvwriter.writerow([f"15-{i}", time_value])

extract_time_and_write_csv('disp')
extract_time_and_write_csv('nodisp')

# Generate the timesDispBetter file
with open('disp.csv', 'r') as dispfile, open('nodisp.csv', 'r') as nodispfile, open('timesDispBetter', 'w') as outfile:
    dispreader = csv.reader(dispfile)
    nodispreader = csv.reader(nodispfile)
    next(dispreader)  # skip headers
    next(nodispreader)  # skip headers
    for disp_row, nodisp_row in zip(dispreader, nodispreader):
        if float(disp_row[1]) < float(nodisp_row[1]):
            outfile.write(f"{disp_row[0]}: {disp_row[1]}s < {nodisp_row[1]}s\n")
