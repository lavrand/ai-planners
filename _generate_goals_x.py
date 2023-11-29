import os
import re

def comment_all_except_nth_goal(original_file_path, new_file_path, n):
    with open(original_file_path, 'r') as file:
        content = file.read()

    goal_section_match = re.search(r'\(:goal \(and(.+?)\)\)', content, re.DOTALL)
    if not goal_section_match:
        print(f"No goal section found in {original_file_path}")
        return

    goal_section = goal_section_match.group(1).strip()
    goals = goal_section.split('\n')
    goals = [goal for goal in goals if goal.strip() and not goal.strip().startswith(';')]

    if len(goals) < n:
        print(f"Not enough goals to keep the {n}th goal in {original_file_path}")
        return

    for i, goal in enumerate(goals, start=1):
        if i != n:
            content = content.replace(goal, ';' + goal)

    with open(new_file_path, 'w') as file:
        file.write(content)

directory_path = '.'  # Path to the directory containing original PDDL files
new_directory_path = './modified_files'  # Path to the directory for modified files

# Create a new directory for modified files
if not os.path.exists(new_directory_path):
    os.makedirs(new_directory_path)

# Counter for the new file names
file_counter = 1

# Loop over each goal number and each file
for goal_number in range(1, 9):  # Goals 1 to 8
    for file_number in range(1, 301):  # Files pfile1 to pfile300
        original_file_name = f'pfile{file_number}'
        new_file_name = f'pfile{file_counter}'
        original_file_path = os.path.join(directory_path, original_file_name)
        new_file_path = os.path.join(new_directory_path, new_file_name)
        comment_all_except_nth_goal(original_file_path, new_file_path, goal_number)
        file_counter += 1
