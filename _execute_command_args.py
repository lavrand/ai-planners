import subprocess
import sys

def execute_command_args(plan, arguments):
    command = plan

    if not isinstance(arguments, list):
        print("Error: arguments must be in a list.", file=sys.stderr)
        sys.exit(1)

    full_command = [command] + arguments

    try:
        print(f"Executing command: {' '.join(full_command)}")  # Print the command for debugging
        process = subprocess.run(full_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # If the command was successful, print the output
        print(process.stdout)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to execute the command. Return code: {e.returncode}", file=sys.stderr)
        print(f"Command output:\n{e.output}", file=sys.stderr)
        print(f"Command stderr:\n{e.stderr}", file=sys.stderr)
        sys.exit(e.returncode)  # Exit with the error code provided by the command

    except Exception as e:
        print(f"An error occurred while trying to run the command: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    PFILEN = 10  # for example
    DOMAIN = 'DepotsTime.pddl'  # for example

    # Explicitly converting PFILEN to string, as the command-line tool might expect string arguments
    execute_command_args('./gen', [str(PFILEN), DOMAIN])
