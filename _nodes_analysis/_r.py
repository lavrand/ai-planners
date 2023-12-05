import os
import subprocess
import time
import pandas as pd
from docx import Document

# Constants
RCLL = "RCLL"

# Function to check if the summary.csv file is populated
def is_summary_populated(file_path):
    return os.path.exists(file_path) and os.path.getsize(file_path) > 0

# Function to reshape the vertical data from summary.csv to horizontal
def reshape_data(df, folder_number):
    # Reshape the DataFrame so that each row becomes a column
    reshaped_df = df.T
    # Reset the index to make the first row as header
    reshaped_df.columns = reshaped_df.iloc[0]
    reshaped_df = reshaped_df.drop(reshaped_df.index[0])
    # Add the folder number as a new column
    reshaped_df['Experiment #'] = folder_number
    return reshaped_df

# Function to rename report.docx and update its content
def rename_and_update_report(nodes_analysis_dir, folder_number):
    old_report_path = os.path.join(nodes_analysis_dir, 'report.docx')
    new_report_path = os.path.join(nodes_analysis_dir, f'{folder_number}.docx')

    # Rename report.docx to {folder_number}.docx
    if os.path.exists(old_report_path):
        os.rename(old_report_path, new_report_path)
        print(f"Renamed report to {new_report_path}")

        # Replace "_nodes_analysis" with "RCLL {folder_number}" in the document
        doc = Document(new_report_path)
        for paragraph in doc.paragraphs:
            if "_nodes_analysis" in paragraph.text:
                paragraph.text = paragraph.text.replace("_nodes_analysis", f"{RCLL} {folder_number}")
        doc.save(new_report_path)
        print(f"Updated contents of {new_report_path}")

# Function to run the report script and collect data
def run_report_and_collect_data(base_dir, output_csv, max_folder_num):
    consolidated_data = []

    for i in range(1, max_folder_num + 1):
        nodes_analysis_dir = os.path.join(base_dir, str(i), '_nodes_analysis')
        report_script = os.path.join(nodes_analysis_dir, '_report.sh')
        summary_csv = os.path.join(nodes_analysis_dir, 'summary.csv')

        # Run report script and rename/update Word document
        if os.path.exists(report_script):
            print(f"Running report script in {nodes_analysis_dir}")
            subprocess.run(['./_report.sh'], cwd=nodes_analysis_dir)

            # Rename and update report.docx
            rename_and_update_report(nodes_analysis_dir, i)

            # Wait until summary.csv is populated
            while not is_summary_populated(summary_csv):
                print(f"Waiting for summary.csv in {nodes_analysis_dir} to be populated...")
                time.sleep(1)

            # Read data from summary.csv
            try:
                df = pd.read_csv(summary_csv, header=None)
                reshaped_df = reshape_data(df, i)
                consolidated_data.append(reshaped_df)
            except Exception as e:
                print(f"Error reading {summary_csv}: {e}")

    # Combine all data into a single DataFrame
    final_df = pd.concat(consolidated_data, ignore_index=True)

    # Save the DataFrame to a CSV file
    final_df.to_csv(output_csv, index=False)
    print(f"Consolidated data written to {output_csv}")

# Set your parameters here
BASE_DIR = "."  # Replace with your actual directory path
OUTPUT_CSV = "consolidated_table.csv"  # Replace with your desired output file path
MAX_FOLDER_NUM = 11  # Replace with the highest number of your folders

run_report_and_collect_data(BASE_DIR, OUTPUT_CSV, MAX_FOLDER_NUM)
