#!/bin/bash

# Define the parameters for each folder
declare -A time_expansions=(
    [1]=10 [2]=25 [3]=50 [4]=100 [5]=200 [6]=300 [7]=500 [8]=1000
    [9]=10 [10]=25 [11]=50 [12]=100 [13]=200 [14]=300 [15]=500 [16]=1000
    [17]=10 [18]=25 [19]=50 [20]=100 [21]=200 [22]=300 [23]=500 [24]=1000
)

declare -A dispatch_threshold=(
    [1]=0.25 [2]=0.25 [3]=0.25 [4]=0.25 [5]=0.25 [6]=0.25 [7]=0.25 [8]=0.25
    [9]=0.1 [10]=0.1 [11]=0.1 [12]=0.1 [13]=0.1 [14]=0.1 [15]=0.1 [16]=0.1
    [17]=0.025 [18]=0.025 [19]=0.025 [20]=0.025 [21]=0.025 [22]=0.025 [23]=0.025 [24]=0.025
)

# Loop through the folders
for i in {1..24}
do
    # Clone the repository into a folder named as the current number
    git clone https://github.com/lavrand/ai-planners.git $i

    # Change directory to _configs within the cloned repository
    cd $i/_configs

    # Run the python script with the specified parameters
    python _update_configs_args.py --time_expansions ${time_expansions[$i]} --dispatch_threshold ${dispatch_threshold[$i]}

    # Submit the job and capture the output
    output=$(sbatch sbatch.sbatch)

    # Extract the job ID from the output
    job_id=$(echo $output | grep -oP '(?<=Submitted batch job )\d+')

    # Print the mapping of folder number to job ID
    echo "$i - $job_id"

    # Go back to the parent directory
    cd ../..
done
