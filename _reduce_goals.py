import os
import random
import re

def comment_half_goals_in_pddl(file_path):
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

    # Randomly select half of the goals to comment out
    goals_to_comment = random.sample(goals, len(goals) // 2)

    for goal in goals_to_comment:
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
    comment_half_goals_in_pddl(os.path.join(directory_path, file_name))
