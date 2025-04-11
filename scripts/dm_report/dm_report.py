# Python script that creates dm report for one subject one task

# Inputs (external)
# events file
# a preprocessed functional image file to get the TR and nscans

# Parameters
# subnum
# task
# output_path
# input_path
# save_pdf
# parameters for rt_data_analysis.main_analysis_code.analyze_lev1.make_desmat_contrasts

# Outputs
# dm_report_{task}_{subnum}.html
# dm_cormat_{task}_{subnum}.csv

# Nice explanation for why we want to end this script with if __name__ == "__main__":
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do

from argparse import ArgumentParser, RawTextHelpFormatter

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
    parser.add_argument(
        'regress_rt',
        choices=['no_rt', 'rt_uncentered', 'rt_centered', 'rt_duration', 'rt_duration_only'],
        help=('Use to specify how rt is/is not modeled. If rt_centered is used '
              'you will potentially have an RT confound in the group models')
    )
    parser.add_argument(
        '--omit_deriv',
        action='store_true',
        help=('Use to omit derivatives for task-related regressors '
             '(typically you would want derivatives)')
    )
    return parser