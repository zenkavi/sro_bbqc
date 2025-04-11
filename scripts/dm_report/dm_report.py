# Python script that creates dm report for one subject one task

# Inputs (external)
# events file
# a preprocessed functional image file to get the TR and nscans

# Parameters
# subnum
# task
# output_path
# input_path
# save_html
# parameters for rt_data_analysis.main_analysis_code.analyze_lev1.make_desmat_contrasts

# Outputs
# derivatives/bbqc/sub-{subnum}/dm_report_{task}_{subnum}.html
# derivatives/bbqc/sub-{subnum}/figures/dm_corheatmap_{task}_{subnum}.png
# derivatives/bbqc/sub-{subnum}/figures/dm_vif_{task}_{subnum}.png
# derivatives/bbqc/sub-{subnum}/dm_cormat_{task}_{subnum}.csv
# derivatives/bbqc/sub-{subnum}/dm_vif_{task}_{subnum}.csv

# Nice explanation for why we want to end this script with if __name__ == "__main__":
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do

from argparse import ArgumentParser, RawTextHelpFormatter
import sys

def get_parser():
    """Build parser object"""
    parser = ArgumentParser(
        prog='dm_report',
        description='dm_report: Creates a dm report for one subject one task',
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        'task',
        choices=['stroop', 'ANT', 'CCTHot', 'stopSignal', 'twoByTwo', 'WATT3',
                 'discountFix', 'DPX', 'motorSelectiveStop'],
        help='Use to specify task.'
    )
    parser.add_argument(
        'subnum',
        action='store',
        type=str,
        help='String indicating subject number',
    )
    # parser.add_argument(
    #     'regress_rt',
    #     choices=['no_rt', 'rt_uncentered', 'rt_centered', 'rt_duration', 'rt_duration_only'],
    #     help=('Use to specify how rt is/is not modeled. If rt_centered is used '
    #           'you will potentially have an RT confound in the group models')
    # )
    # parser.add_argument(
    #     '--omit_deriv',
    #     action='store_true',
    #     help=('Use to omit derivatives for task-related regressors '
    #          '(typically you would want derivatives)')
    # )
    parser.add_argument(
        'input_path',
        action='store',
        type=str,
        help='Root directory for input files.',
    )
    parser.add_argument(
        'output_path',
        action='store',
        type=str,
        help='Directory for output files.',
    )
    parser.add_argument(
        '--save_html',
        action='store_true',
        help=('Save subject level html report. ')
    )
    return parser

def plot_dm_cormat(correlation_matrix, vif_data):

    correlation_matrix = correlation_matrix.dropna(axis=0, how='all')
    correlation_matrix = correlation_matrix.dropna(axis=1, how='all')

    f = plt.figure(figsize=(5, 3))

    f.set_figheight(11)
    f.set_figwidth(15)

    plt.subplot(2, 2, 1)
    sns.heatmap(correlation_matrix, cmap = "coolwarm",)
    plt.title("Heatmap of Correlation Matrix")

    plt.subplot(2, 2, 2)
    sns.barplot(x="VIF", y="Variable", data=vif_data, palette="coolwarm", orient="h")
    plt.axvline(x=math.log(5), color='r', linestyle='--', label="Moderate Multicollinearity (log(VIF)=1.6)")
    plt.axvline(x=math.log(10), color='black', linestyle='--', label="High Multicollinearity (log(VIF)=2.3)")
    plt.xlabel("Log of Variance Inflation Factor (VIF)")
    plt.ylabel("Predictor Variables")
    plt.title("VIF Values for fMRI GLM Variables")
    plt.legend()

    plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1, hspace=0.4, wspace=0.5)

if __name__ == "__main__":

    from rt_data_analysis.main_analysis_code.analyze_lev1 import make_desmat_contrasts, get_files, get_nscans
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    import math
    
    opts = get_parser().parse_args(sys.argv[1:])
    subid = opts.subid
    task = opts.task
    input_path = opts.input_path
    output_path = opts.output_path
    save_html = opts.save_html

    # Does it matter for the VIF to include all possible RT regressors and derivatives?
    # regress_rt = opts.regress_rt 
    # if opts.omit_deriv:
    #     add_deriv = 'deriv_no'
    # else:
    #     add_deriv = 'deriv_yes'

    # files = get_files(root, subid, task) 

    n_scans = get_nscans(files['data_file'])
    
    design_matrix, contrasts, percent_junk, percent_high_motion, tr = make_desmat_contrasts(root, task, 
        files['events_file'], add_deriv, n_scans, files['confounds_file'], regress_rt
    )
    design_matrix['constant'] = 1
    design_matrix.drop(columns=['csf', 'white_matter'], inplace=True)

    correlation_matrix = design_matrix.corr(numeric_only=True)
    # Save this correlation_matrix (with all columns) csv to output_path

    vif_data = pd.DataFrame()
    vif_data["Variable"] = design_matrix.columns
    vif_data["VIF"] = [math.log(variance_inflation_factor(design_matrix.values, i)) for i in range(design_matrix.shape[1])]

    plot_dm_cormat(correlation_matrix, vif_data)

    if save_html:
        # Save the html report to output_path
        print("Saving HTML report...")