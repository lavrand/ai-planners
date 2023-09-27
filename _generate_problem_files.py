# Define the name of the source file and its content
source_file_name = "withdeadlines-ontime-pfile15-"

with open(source_file_name, 'r') as source_file:
    content = source_file.read()

# Create 100 copies with the same content
for i in range(1, 101):
    target_file_name = f"withdeadlines-ontime-pfile15-{i}"
    with open(target_file_name, 'w') as target_file:
        target_file.write(content)

print("Files created successfully!")