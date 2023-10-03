import csv
import os

# Load the data from output_full.csv
data = []
with open('output_full.csv', 'r') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)  # Skip the header
    data = list(csv_reader)

# Process the data
both_solved = [row for row in data if row[1] not in ['9999', '99999'] and row[2] not in ['9999', '99999']]
disp_only = [row for row in data if row[1] not in ['9999', '99999'] and row[2] in ['9999', '99999']]
nodisp_only = [row for row in data if row[1] in ['9999', '99999'] and row[2] not in ['9999', '99999']]


avg_disp = round(sum(float(row[1]) for row in both_solved) / len(both_solved), 2)
avg_nodisp = round(sum(float(row[2]) for row in both_solved) / len(both_solved), 2)
avg_ratio = round(sum(float(row[1]) / float(row[2]) for row in both_solved) / len(both_solved), 2)


# Determine the parent folder (two levels up)
folder_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath("output_full.csv"))))

# Create the new CSV
output_filename = "summary.csv"
with open(output_filename, 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['Original instance', folder_name])
    csv_writer.writerow(['Number of permutations solved by both disp and nodisp', len(both_solved)])
    csv_writer.writerow(['Number of permutations solved only by disp', len(disp_only)])
    csv_writer.writerow(['Number of permutations solved only by nodisp', len(nodisp_only)])
    csv_writer.writerow(['Average solution time for disp on permutations solved by both disp and nodisp', avg_disp])
    csv_writer.writerow(['Average solution time for nodisp on permutations solved by both disp and nodisp', avg_nodisp])
    csv_writer.writerow(['Average speedup ratio for disp over permutations solved by both disp and nodisp', avg_ratio])

print(f"Summary data has been written to {output_filename}")
