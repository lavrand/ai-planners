import csv
import os

NODISP_ROW = 3

DISP_ROW = 2

ROUND = 2

# Load the data from output_full.csv
data = []
with open('output_full.csv', 'r') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)  # Skip the header
    data = list(csv_reader)

# Process the data
both_solved = [row for row in data if row[DISP_ROW] not in ['9999', '99999'] and row[NODISP_ROW] not in ['9999', '99999']]
disp_only = [row for row in data if row[DISP_ROW] not in ['9999', '99999'] and row[NODISP_ROW] in ['9999', '99999']]
nodisp_only = [row for row in data if row[DISP_ROW] in ['9999', '99999'] and row[NODISP_ROW] not in ['9999', '99999']]


# Calculate the sum and length once to avoid repeating these operations
sum_disp = sum(float(row[DISP_ROW]) for row in both_solved)
sum_nodisp = sum(float(row[NODISP_ROW]) for row in both_solved)
len_both_solved = len(both_solved)

# Use a conditional expression to check for a zero denominator
avg_disp = 0 if len_both_solved == 0 else round(sum_disp / len_both_solved, ROUND)
avg_nodisp = 0 if len_both_solved == 0 else round(sum_nodisp / len_both_solved, ROUND)

# Check if len(both_solved) is 0 to avoid ZeroDivisionError
avg_ratio = 0 if len(both_solved) == 0 else round(
    sum(
        0 if float(row[NODISP_ROW]) == 0 else float(row[DISP_ROW]) / float(row[NODISP_ROW])
        for row in both_solved
    ) / len(both_solved),
    ROUND + 2
)

# Determine the parent folder (two levels up)
folder_name = os.path.basename(os.path.dirname(os.path.abspath("output_full.csv")))

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
