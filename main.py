import subprocess
import re

# Define the shell script path and the Perl script path
shell_script_path = './run.sh'
perl_script_path = './add_initially_on_time'

# Define the CSV file to store the times
csv_file_path = 'times.csv'

# Write headers to the CSV file
with open(csv_file_path, 'w') as csv_file:
    csv_file.write('File, Situated Temporal Planning, Offline Planning, Situated Planning\n')

# Loop through the range of files
__start = 1
__stop = 4
for i in range(__start, __stop):
    input_file_name = f'pfile{i}'
    modified_input_file_name = f'withdeadlines-ontime-{input_file_name}'
    output_file_path = f'report{i}.txt'

    # Invoke the Perl script to modify the pfile
    subprocess.run([perl_script_path, input_file_name, modified_input_file_name])

    # Run the shell script and capture the output for the modified pfile
    with open(output_file_path, 'w') as output_file:
        subprocess.run([shell_script_path, modified_input_file_name], stdout=output_file, stderr=subprocess.STDOUT)

    # Extract times from the report
    with open(output_file_path, 'r') as report_file:
        content = report_file.read()
        times = re.findall(r'; Time (\d+\.\d+)', content)

        # Check if we found exactly 3 times
        if len(times) == 3:
            with open(csv_file_path, 'a') as csv_file:
                csv_file.write(f'{modified_input_file_name}, {times[0]}, {times[1]}, {times[2]}\n')
        else:
            print(f"Unexpected number of times in {output_file_path}. Expected 3, found {len(times)}.")



