#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job. main - 7 days time limit
#SBATCH --time 1-12:50:00 ### limit the time of job running. Make sure it is not greater than the partition time limit!! Format: D-H:MM:SS
#SBATCH --job-name my_job ### name of the job. replace my_job with your desired job name
#SBATCH --output /cs_storage/seanmar/pancake/my_job-id-%J.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=seanmar@post.bgu.ac.il ### users email for sending job status notifications
#SBATCH --mail-type=END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4 # 6 cpus per task – use for multithreading, usually with --tasks=1
#SBATCH --tasks=1 # 2 processes – use for processing of few programs concurrently in a job (with srun). Use just 1 otherwise
### Print some data to output file ###
### Start you code below ####
### Start your code below ####
module load anaconda
source activate my_env
###python -u -m memory_profiler "/cs_storage/seanmar/pancake/pancake.py" 1912 1950
###python -u -m memory_profiler "/cs_storage/seanmar/pancake/Remaining_Search_Effort_Estimator/ML_Methods.py" 0 300
###python -u -m memory_profiler "/cs_storage/seanmar/pancake/Remaining_Search_Effort_Estimator/main.py"

###echo $curr_index
python -u -m memory_profiler "/cs_storage/seanmar/pancake/Remaining_Search_Effort_Estimator/ML_Methods.py" 0 100 10000 &
###python -u -m memory_profiler "/cs_storage/seanmar/pancake/Remaining_Search_Effort_Estimator/ML_Methods.py" 2 200 1000 &
###python -u -m memory_profiler "/cs_storage/seanmar/pancake/Remaining_Search_Effort_Estimator/ML_Methods.py" 0 300 1000 &

wait
###
###python -u -m memory_profiler "/cs_storage/seanmar/pancake/Remaining_Search_Effort_Estimator/ML_Methods.py" 1 100 &
###python -u -m memory_profiler "/cs_storage/seanmar/pancake/Remaining_Search_Effort_Estimator/ML_Methods.py" 1 200 &
###python -u -m memory_profiler "/cs_storage/seanmar/pancake/Remaining_Search_Effort_Estimator/ML_Methods.py" 1 300 &
###python -u -m memory_profiler "/cs_storage/seanmar/pancake/Remaining_Search_Effort_Estimator/ML_Methods.py" 2 100 &
###python -u -m memory_profiler "/cs_storage/seanmar/pancake/Remaining_Search_Effort_Estimator/ML_Methods.py" 2 200 &
###python -u -m memory_profiler "/cs_storage/seanmar/pancake/Remaining_Search_Effort_Estimator/ML_Methods.py" 2 300 &
