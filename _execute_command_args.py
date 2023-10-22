import subprocess
import sys

def execute_command_args(plan, arguments):
    # Command to be executed
    command = plan

    # Ensure that 'arguments' is a list to allow multiple arguments
    if not isinstance(arguments, list):
        print("Error: arguments must be in a list.", file=sys.stderr)
        sys.exit(1)

    # Construct the full command by concatenating the command and its arguments
    full_command = [command] + arguments

    try:
        # Executing the command
        process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Communicate will wait for the process to finish and get the output
        stdout, stderr = process.communicate()

        # Check if the command was successful
        if process.returncode != 0:
            print(f"An error occurred while trying to execute the command: {stderr.decode()}", file=sys.stderr)
            sys.exit(process.returncode)  # Exit with the error code provided by the command

        # If the command was successful, print the output
        print(stdout.decode())

    except Exception as e:
        print(f"An error occurred while trying to run the command: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Exit with a general error code

if __name__ == "__main__":
    # Example usage:
    # Replace 'my_executable_plan' with your actual command
    # and ['arg1', 'arg2'] with your actual arguments list.
    execute_command_args('./gen', ['10', 'DepotsTime.pddl'])
