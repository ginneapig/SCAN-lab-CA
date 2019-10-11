'''
# Annie Gao
# Created: 10/10/2019
# Last edited: 10/10/2019

This program's purpose is to upload ANAM and PAI files,
both usually in PDF format, to REDCap for the TBI Model arm
of the SCAN lab.'''
##Currently only uploading PAI files if .txt type. 
##For now, must place program in the same folder as the PAI file to run.

import csv

def main():
    pai_file = 'TBI_999.txt'
    # may remove this list later
    
    fixed_headers, fixed_entries = org_pai(pai_file)
    create_pai_csv(fixed_headers, fixed_entries)




def org_pai(pai_file):
    '''This takes a file name and attempts opening it.
    Two lists removing unnecessary data are created, one being
    the headers in proper format, and one being the numerical data.
    PARAM: string of PAI file name
    RETURN: dictionary of PAI data'''
    ##Note: current file doesn't have 106 entries, but
    ##may be faulty.
    total_pai_entries = 106
    try:
        file_content = open(pai_file).readlines()
    except:
        print('File not found.')

    headers = file_content[0].split(',')
    entries = file_content[1].split(',')
    
    fixed_headers = []
    fixed_entries = []
    for i in range(12, len(headers)-2): # skip non-pai data headers
        curr_header = headers[i].lower()
        new_header = ''
        add = ''
        if (curr_header[-1] == 'r'):
            add = '_rawscore'
        elif (curr_header[-1] == 't'): # not else to avoid extraneous items
            add = '_tscore'

        if (len(curr_header) == 5):
            new_header = curr_header[0:3]
        elif (len(curr_header) == 7): # not else to avoid extraneous items
            new_header = curr_header[0:5]

        if (add != ''): # ensure this was pai data header
            fixed_headers.append(new_header + add)
            fixed_entries.append(entries[i])

    return fixed_headers, fixed_entries

def create_pai_csv(fixed_headers, fixed_entries):
    '''Opens a new CSV file and writes the row of headers as well as
    the row of data for one participant.'''
    with open('PAI_upload.csv', mode='w') as csvfile:
        pai_writer = csv.writer(csvfile, delimiter=',')
        pai_writer.writerow(fixed_headers)
        pai_writer.writerow(fixed_entries)

    csvfile.close()
    

main()