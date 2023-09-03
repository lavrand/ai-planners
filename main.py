import subprocess
import re

# Define the shell script path
shell_script_path = './run.sh'

# Define the CSV file to store the times
csv_file_path = 'times.csv'

# Write headers to the CSV file
with open(csv_file_path, 'w') as csv_file:
    csv_file.write('File, Situated Temporal Planning, Offline Planning, Situated Planning\n')

# Loop through the range of files
for i in range(1, 10):
    input_file_name = f'pfile{i}'
    output_file_path = f'report{i}.txt'

    # Run the shell script and capture the output for each file
    with open(output_file_path, 'w') as output_file:
        subprocess.run([shell_script_path, input_file_name], stdout=output_file, stderr=subprocess.STDOUT)

    # Extract times from the report
    with open(output_file_path, 'r') as report_file:
        content = report_file.read()
        times = re.findall(r'; Time (\d+\.\d+)', content)

        # Check if we found exactly 3 times
        if len(times) == 3:
            with open(csv_file_path, 'a') as csv_file:
                csv_file.write(f'{input_file_name}, {times[0]}, {times[1]}, {times[2]}\n')
        else:
            print(f"Unexpected number of times in {output_file_path}. Expected 3, found {len(times)}.")



