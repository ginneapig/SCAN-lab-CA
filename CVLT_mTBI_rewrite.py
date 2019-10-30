# Annie Gao
# anniegao@email.arizona.edu
# CVLT file reading fixing
# 10/23/2019

import csv
import os
import getpass
import io
import itertools
from collections import OrderedDict

def main():
    CVLT_filepath = './'
    output_path = './CVLT_mTBI_Data.csv'
    
    CVLT_files = org_CVLT(CVLT_filepath) # list of file names
    all_CVLT_dict = collect_files(CVLT_files)

def org_CVLT(CVLT_filepath):
    '''Collects names of all files with ptp data and returns it.'''
    CVLT_files = []
    for filename in os.listdir(CVLT_filepath):
        if (filename.endswith('.csv')
            and filename.startswith('CVLT_TBI_Model')
            and '202' not in filename): # skipping 202, has decoding error
            CVLT_files.append(filename)

    return CVLT_files

def sort_file(file_content):
    '''Takes the list of lines read from one CSV file and sorts it.
    Returns the dictionary of items.
    PARAM: list of CSV file content
    RETURN: dictionary of CVLT headers keyed to corresponding data for one ptp'''
    core_trials = ['1', '2', '3', '4', '5', 'B']
    short_trials = ['short_delay_fr_raw', 'short_delay_fr_ss', 'short_delay_cr_raw', 'short_delay_cr_ss']
    long_trials = ['long_delay_fr_raw', 'long_delay_fr_ss', 'long_delay_cr_raw', 'long_delay_cr_ss']
    # short delay FR correct raw, correct std; CR correct raw, cor std;
    # long delay ...
    # FR intrusions raw, intrusion std;
    # CR intrusions ...
    # total intrusions...
    # total repetitions...
    # long-delay recognitions hits raw, std;
    # long delay recognition false positives ...
    # long-delay forced choice recognitions accuracy raw
    # form status: 2
    ptp_dict = {}
    for line in file_content:
        split_line = line.split()
        for header in core_trials:
            if ('Trial {}'.format(header) in line):
                if (header != 'B'):
                    header_raw = 'trial_' + header + '_fr_raw'
                    header_ss = 'trial_' + header + '_fr_ss'
                else:
                    header_raw = 'list_b_fr_raw'
                    header_ss = 'list_b_fr_ss'

                correct_raw = split_line[2]
                correct_std = split_line[3]
                
                # below: ensure data is not replaced
                if (header_raw not in ptp_dict or header_ss not in ptp_dict): 
                    ptp_dict[header_raw] = correct_raw
                    ptp_dict[header_ss] = correct_std

    
        if ('Trials 1-5 Total' in line):
            if ('trial_1_5_fr_total_raw' not in ptp_dict):
                ptp_dict['trial_1_5_fr_total_raw'] = split_line[3]
                ptp_dict['trial_1_5_fr_total_ss'] = split_line[4]

        elif ('Short Delay Free' in line and 'vs.' not in line):
            ptp_dict[short_trials[0]] = split_line[4]
            ptp_dict[short_trials[1]] = split_line[5]

        elif ('Short Delay Cued' in line):
            ptp_dict[short_trials[2]] = split_line[4]
            ptp_dict[short_trials[3]] = split_line[5]

        elif ('Long Delay Free' in line and 'vs.' not in line):
            ptp_dict[long_trials[0]] = split_line[4]
            ptp_dict[long_trials[1]] = split_line[5]
    
    
    return ptp_dict
  
def collect_files(CVLT_files):
    '''Collects all participants' data in a dictionary by calling
    a helper function and returns the dictionary.
    PARAM: list of file names
    RETURN: dictionary of participants keyed to a dictionary of their data'''
    all_CVLT_dict = {}
    for file in CVLT_files:
        # temp insert below:
        if ('291' in file):
            file_content = open(file).readlines()
            ptp_dict = sort_file(file_content) # calls helper fxn
            ptp_num = file[-7:-4].strip('_') # 2-digit nums include excess
            all_CVLT_dict[ptp_num] = ptp_dict

            print(ptp_dict)

    return all_CVLT_dict
        

main()
