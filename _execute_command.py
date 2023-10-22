import subprocess
import sys


def execute_command(plan, argument):
    # Command to be executed
    command = plan
    argument = argument

    # Construct the full command
    full_command = [command, argument]

    try:
        # Executing the command
        process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Communicate will wait for the process to finish and get the output
        stdout, stderr = process.communicate()

        # Check if the command was successful
        if process.returncode != 0:
            print("An error occurred while trying to execute the command:", stderr.decode(), file=sys.stderr)
            sys.exit(process.returncode)  # Exit with the error code provided by the command

        # If the command was successful, print the output
        print(stdout.decode())

    except Exception as e:
        print(f"An error occurred while trying to run the command: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Exit with a general error code


if __name__ == "__main__":
    execute_command("./run-planner-to-get-initial-plan", "ontime-pfile10")
    # execute_command("./add_initially_on_time", "pfile10")
