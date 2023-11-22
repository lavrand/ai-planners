import os
import re

# The N-th goal to keep uncommented
X = 2  # Example value


def comment_all_except_nth_goal(file_path, n):
    with open(file_path, 'r') as file:
        content = file.read()

    # Find the goal section
    goal_section_match = re.search(r'\(:goal \(and(.+?)\)\)', content, re.DOTALL)
    if not goal_section_match:
        print(f"No goal section found in {file_path}")
        return

    goal_section = goal_section_match.group(1).strip()
    goals = goal_section.split('\n')

    # Filter out empty lines and comments
    goals = [goal for goal in goals if goal.strip() and not goal.strip().startswith(';')]

    # Check if there is a goal at the N-th index
    if len(goals) < n:
        print(f"Not enough goals to keep the {n}th goal in {file_path}")
        return

    # Comment out all goals except the N-th one
    for i, goal in enumerate(goals, start=1):
        if i != n:
            content = content.replace(goal, ';' + goal)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)


# Path to the directory containing PDDL files
directory_path = '.'


# List all PDDL files
pddl_files = [f for f in os.listdir(directory_path) if re.match(r'pfile\d+', f)]

# Process each file
for file_name in pddl_files:
    comment_all_except_nth_goal(os.path.join(directory_path, file_name), X)
