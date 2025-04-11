# Shell script that will pipe input arguments to dm_report.sbatch and submit the job
# Should work both for individual subjects/tasks and for all subjects/tasks
# When running for "all" need to decide on if we'll have a separate task list that read in line by line
# or if we'll have a for loop in this script

# For example see https://github.com/zenkavi/DescribedVsLearned_beh/blob/master/analysis/helpers/ddModels/cluster_scripts/run_ddm_Roptim.sh