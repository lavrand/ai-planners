import os

# Define the name of the source file and its content
source_file_name = "withdeadlines-ontime-pfile15-"

# Check if source file exists
if not os.path.exists(source_file_name):
    print(f"Error: {source_file_name} does not exist.")
    exit()

with open(source_file_name, 'r') as source_file:
    content = source_file.read()

# Create 100 copies with the same content
for i in range(1, 101):
    target_file_name = f"withdeadlines-ontime-pfile15-{i}"
    with open(target_file_name, 'w') as target_file:
        target_file.write(content)

# Verification step
all_files_match = True
for i in range(1, 101):
    target_file_name = f"withdeadlines-ontime-pfile15-{i}"

    with open(target_file_name, 'r') as target_file:
        target_content = target_file.read()

        if target_content != content:
            print(f"Content mismatch in {target_file_name}")
            all_files_match = False

if all_files_match:
    print("Files created and verified successfully!")
else:
    print("Some files do not match the original content!")
