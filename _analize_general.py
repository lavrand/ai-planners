import os
import shutil
import subprocess

# Get the total number of archive folders (assuming they are sequentially named and start from 1)
N = 22  # Set this to the actual number of archive folders you have

# List of scripts to copy
scripts = [
    '_analyze.py',
    '_generate_summary.py',
    '_normalize.py',
    '_pressure.py',
    '_report_root_folder_full.py',
    '_xyplot.py'
]

# Function to copy scripts to target folder and run _analyze.py
def process_folder(folder_name):
    for script in scripts:
        # Copy each script to the target folder
        shutil.copy(os.path.join(root_dir, script), os.path.join(folder_name, script))

    # Change to the target folder to run _analyze.py
    os.chdir(folder_name)
    subprocess.run(['python3', '_analyze.py'])
    os.chdir(root_dir)  # Change back to root directory


# Main process
root_dir = os.getcwd()  # Assuming scripts are located in the current working directory

# Process each archive folder
for i in range(1, N + 1):
    folder_name = f'archive_pfile_{i}'
    process_folder(folder_name)

# Create summary folder and process each archive folder again to move generated files
summary_dir = os.path.join(root_dir, 'summary')
os.makedirs(summary_dir, exist_ok=True)

for i in range(1, N + 1):
    folder_name = f'archive_pfile_{i}'
    new_folder_name = f'pfile_{i}'
    new_folder_path = os.path.join(summary_dir, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)

    # Copy generated files to the new folders in the summary directory
    for file_name in ['disp_vs_nodisp_plot.png', 'summary.csv']:
        shutil.copy(os.path.join(folder_name, file_name), os.path.join(new_folder_path, file_name))
