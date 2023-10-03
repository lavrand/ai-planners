import os

folder_path = './'  # Current directory. Change this to your folder path if different.

# List all files in the directory
files_in_directory = os.listdir(folder_path)

# Filter for files which end in .zip
filtered_files = [file for file in files_in_directory if file.endswith(".gz")]

# Delete each .zip file
for file in filtered_files:
    os.remove(os.path.join(folder_path, file))

print("All .gz files have been removed!")
