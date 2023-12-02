#!/bin/bash

# Run Python scripts one by one
python _nodes_analysis.py
python _simulated_time.py
python _generate_summary.py
python _xyplot.py

# Check if the required files exist
if [[ -f "disp_vs_nodisp_plot.png" && -f "summary.csv" && -f "Simulated_Time_Solution_Found.csv" ]]; then
    # Use a Python script to insert the image and tables into a Word document
    python - <<EOF
import pandas as pd
from docx import Document
from docx.shared import Inches

# Function to add a table from CSV to the document
def add_table_from_csv(doc, file_path):
    df = pd.read_csv(file_path)
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

# Create a new Word document
doc = Document()

# Insert the image
doc.add_picture('disp_vs_nodisp_plot.png', width=Inches(6))

# Add a page break
doc.add_page_break()

# Insert the first table
add_table_from_csv(doc, 'summary.csv')

# Add a page break
doc.add_page_break()

# Insert the second table
add_table_from_csv(doc, 'Simulated_Time_Solution_Found.csv')

# Save the document
doc.save('report.docx')
EOF

    echo "Report generated successfully as report.docx"
else
    echo "Required files not found."
fi
