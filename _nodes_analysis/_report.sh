#!/bin/bash

# Run Python scripts one by one
python _nodes_analysis_deadlines.py
python _simulated_time.py
python _generate_summary.py
python _xyplot.py

# Check if the required files exist
if [[ -f "disp_vs_nodisp_plot.png" && -f "summary.csv" ]]; then
    # Use a Python script to insert the image and table into a Word document
    python - <<EOF
import pandas as pd
from docx import Document
from docx.shared import Inches

# Create a new Word document
doc = Document()

# Insert the image
doc.add_picture('disp_vs_nodisp_plot.png', width=Inches(6))

# Insert the table from the CSV file
df = pd.read_csv('summary.csv')
table = doc.add_table(rows=1, cols=len(df.columns))
table.style = 'Table Grid'

# Add the header rows.
for j in range(len(df.columns)):
    table.cell(0,j).text = df.columns[j]

# Add the rest of the data frame
for i in range(df.shape[0]):
    row_cells = table.add_row().cells
    for j in range(df.shape[1]):
        row_cells[j].text = str(df.values[i,j])

# Save the document
doc.save('report.docx')
EOF

    echo "Report generated successfully as report.docx"
else
    echo "Required files not found."
fi