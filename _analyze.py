import subprocess
import sys

# Check if a command line argument has been provided
if len(sys.argv) < 2:
    print("Usage: python _analyze.py <timeout>")
    sys.exit(1)

# The second command line argument is expected to be the config file name
MAX = sys.argv[1]

def run_script(script_name):
    """
    Run a python script and wait for it to complete.

    Parameters:
    script_name (str): The name of the script to run.
    """
    # Command to run a python script
    command = ['python3', script_name]

    # Run the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Wait for the process to complete and capture the output and errors
    stdout, stderr = process.communicate()

    # Check if the process has ended without errors
    if process.returncode == 0:
        print(f'Successfully ran {script_name}:')
        print(stdout)
    else:
        print(f'Failed to run {script_name}:')
        print(stderr)

def main():
    # Define the directory containing the scripts - replace with your path

    script_dir = os.getcwd() # script_dir = '/home/andrey/analysis/Depots/22.10.23 00-49'
    # Define the scripts to run in order

    scripts = [
        '_report_root_folder_full.py',
        '_normalize.py',
        '_pressure.py',
        '_generate_summary.py',
        '_xyplot.py'
    ]

    # Define a function to run scripts with optional parameters
    def run_script(script_name, param=None):
        if param:
            # If there is a parameter, include it in the command
            command = f"python {script_name} {param}"
        else:
            # If no parameter, just run the script without any
            command = f"python {script_name}"

        # Execute the command
        os.system(command)


    # Change the current working directory to the script directory
    try:
        os.chdir(script_dir)
    except Exception as e:
        print(f"An error occurred when changing the directory: {str(e)}")
        return

    # Execute each script in sequence
    for script in scripts:
        if script == '_xyplot.py':
            # If the script is _xyplot.py, pass MAX as a parameter
            run_script(script, MAX)
        else:
            # Otherwise, run the script without any parameters
            run_script(script)


if __name__ == "__main__":
    import os
    main()
