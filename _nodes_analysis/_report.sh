#!/bin/bash

# Run Python scripts one by one
python _nodes_analysis.py
python _simulated_time.py
python _generate_summary.py
python _xyplot.py

# Check if the required files exist
if [[ -f "disp_vs_nodisp_plot.png" && -f "summary.csv" && -f "Simulated_Time_Solution_Found.csv" ]]; then
    # Use the separate Python script to insert the image and tables into a Word document
    python _create_report.py

    echo "Report generated successfully as report.docx"
else
    echo "Required files not found."
fi
