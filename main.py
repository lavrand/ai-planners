import subprocess

# Define the shell script path
shell_script_path = './run.sh'

# Loop through the range of files
for i in range(1, 21):
    input_file_name = f'pfile{i}'
    output_file_path = f'report{i}.txt'

    # Run the shell script and capture the output for each file
    with open(output_file_path, 'w') as output_file:
        subprocess.run([shell_script_path, input_file_name], stdout=output_file, stderr=subprocess.STDOUT)

