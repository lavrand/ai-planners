import os


def rename_files_in_folder(folder_path):
    """
    Renames all files in the specified folder to pfile1, pfile2, ..., pfileX.
    :param folder_path: Path to the folder whose files are to be renamed.
    """
    # List all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Rename each file
    for i, file in enumerate(files, start=1):
        new_name = f"pfile{i}"
        old_file_path = os.path.join(folder_path, file)
        new_file_path = os.path.join(folder_path, new_name)

        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed {file} to {new_name}")

# Example usage
# Please replace 'your_folder_path' with the actual path of the folder you want to rename files in.
rename_files_in_folder('problem_files/rcll_3robots')