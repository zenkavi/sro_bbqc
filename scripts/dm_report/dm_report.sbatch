#!/bin/bash
#SBATCH --job-name=dm_report_{TASK}_{SUBNUM}
#SBATCH --partition=main
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8GB
#SBATCH --time=1:00:00
#SBATCH --output=/hopper/groups/enkavilab/.out/dm_report_{TASK}_{SUBNUM}_%j.out
#SBATCH --error=/hopper/groups/enkavilab/.err/dm_report_{TASK}_{SUBNUM}_%j.err
#SBATCH --mail-user=zenkavi@cmc.edu
#SBATCH --mail-type=FAIL

# Job that calls dm_report.py to compute and save dm repot for one subject and one task

# Define input arguments (some place holders)
SUBNUM=...
TASK=...
INPUT_PATH=...
OUTPUT_PATH=...
SAVE_PDF=...

# How should we call the python script?
# Activate a virtual env? Docker image?

