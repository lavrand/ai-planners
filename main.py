import subprocess
import re

# Define the shell script path, the add_initially_on_time Perl script path, and the getgoaltimes Perl script path
shell_script_path = './run.sh'
add_initially_on_time_script_path = './add_initially_on_time'
getgoaltimes_script_path = './getgoaltimes'

# Define the CSV file to store the times
csv_file_path = 'times.csv'

# Write headers to the CSV file
with open(csv_file_path, 'w') as csv_file:
    csv_file.write('File, Online Planning, Offline Planning, Situated Planning\n')

# Define the start and stop range for the loop
__start = 2
__stop = 15

# Loop through the specified range of files
for i in range(__start, __stop + 1):
    input_file_name = f'pfile{i}'
    ontime_file_name = f'ontime-{input_file_name}'
    withdeadlines_file_name = f'withdeadlines-{ontime_file_name}'
    output_file_path = f'report{i}.txt'

    # Invoke the add_initially_on_time Perl script to create the ontime-pfile
    subprocess.run([add_initially_on_time_script_path, input_file_name, ontime_file_name])

    # Invoke the getgoaltimes Perl script to modify the ontime-pfile to withdeadlines-ontime-pfile
    subprocess.run([getgoaltimes_script_path, ontime_file_name, withdeadlines_file_name])

    # Run the shell script and capture the output for the withdeadlines-ontime-pfile
    with open(output_file_path, 'w') as output_file:
        subprocess.run([shell_script_path, withdeadlines_file_name], stdout=output_file, stderr=subprocess.STDOUT)

    # Extract times from the report
    with open(output_file_path, 'r') as report_file:
        content = report_file.read()
        times = re.findall(r'; Time (\d+\.\d+)', content)

        # Check if we found exactly 3 times
        if len(times) == 3:
            with open(csv_file_path, 'a') as csv_file:
                csv_file.write(f'{withdeadlines_file_name}, {times[0]}, {times[1]}, {times[2]}\n')
        else:
            print(f"Unexpected number of times in {output_file_path}. Expected 3, found {len(times)}.")
