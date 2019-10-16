# Computerized Assessments Upload Script
# Annie Gao
# Created: 09/25/2019
# Last edited: 10/10/2019

'''Interactive script: user inputs type of file to input and participant
IDs of those desired to upload. Runs on several while loops to prompt user
continuously until finished.'''

import csv

def main():
    want_to_upload = True   # flag for running while loop
    while (want_to_upload == True):
        test_type = input("Enter the name of the file type you want to upload. " +
                      "This includes GNG, PAI, PVT: ")
        test_type = test_type.strip().lower()

        if (test_type == 'pvt'):       
            orig_doc, new_doc = run_pvt()
            # static list of PVT headers
            new_doc_headers = ['participantid', 'sum_tooearly', 'sum_lapse',
                               'sum_toofast', 'sum_falsestarts', 'avrt_nofalsestarts',
                               'pvt_rt_stdev', 'av_speed', 'pvt_complete']
            pvt_upload(orig_doc, new_doc, new_doc_headers)

        elif (test_type == 'gng'):
            orig_doc, new_doc = run_gng()
            # static list of GNG headers
            new_doc_headers = ['participantid', 'go_accuracy', 'go_rt',
                               'nogo_accuracy', 'nogo_rt', 'gonogo_complete']
            gng_upload(orig_doc, new_doc, new_doc_headers)

        elif (test_type == 'pai'):
            file_content = run_pai()
            fixed_headers, fixed_entries = org_pai(file_content)
            pai_upload(fixed_headers, fixed_entries)
            check_pai_template(fixed_headers)
        else:
            print('File type does not exist/was entered incorrectly. Please try again.')

        more_files = input('Would you like to upload more files (yes/no)? ')
        if (more_files.strip().lower() == 'no'): # changes flag, exits loop
            want_to_upload = False

def run_pvt():
    '''Attempts to open the PVT file as user entered. If file exists,
    a new CSV file is created with proper headers.
    PARAM: none
    RETURN: original CSV file as list, new CSV file (empty)'''
    current_pvt = input("Current PVT file (do not include .csv)? ")
    try: 
        orig_doc = open('../PVT/REDCAP/' + current_pvt + '.csv')
    except FileNotFoundError as e:
        print("File not found. Please try again.")

    orig_doc = orig_doc.readlines()
    new_doc = open('PVT_entries.csv', mode='w') # creates new file each time
    
    return orig_doc, new_doc
    

def pvt_upload(orig_doc, new_doc, new_doc_headers):
    '''Uses the csv library to write to a file for upload to REDCAP.
    Requires user to enter participant ID one at a time. Exits while loop when finished.
    PARAM: list of original PVT document entries, new document to write to,
        list of headers for REDCAP upload
    RETURN: none as of currently'''
    pvt_writer = csv.writer(new_doc, delimiter=',') #, quotechar='"', quoting=csv.QUOTE_MINIMAL
    pvt_writer.writerow(new_doc_headers) # writes the headers for uploading

    more_ptp = 'yes'
    while (more_ptp.lower() == 'yes'):
        new_ptp = input('Enter the participant ID you would like uploaded: ')
        for i in range(1, len(orig_doc)):
            row = orig_doc[i].split(',')
            if (row[1] == new_ptp):
                new_row = [row[1], row[3], row[4], row[5], row[6], row[8], row[9], row[10], 'Complete']
                pvt_writer.writerow(new_row)
        more_ptp = input('More participants (yes/no)? ')
        
    print('Upload the file called \'PVT_entries.csv\' located directly inside the ' +
          '\'Organized by assessment\' folder to REDCAP.')


def run_gng():
    '''Attempts to open the GNG file as user entered. If file exists,
    a new CSV file is created with proper headers.
    PARAM: none
    RETURN: original CSV file as list, new CSV file (empty)'''
    current_gng = input("Current GNG file (do not include .csv)? ")
    try: 
        orig_doc = open('../GNG/REDCAP/' + current_gng + '.csv')
    except FileNotFoundError as e:
        print("File not found. Please try again.")

    orig_doc = orig_doc.readlines()
    new_doc = open('GNG_entries.csv', mode='w') # creates new file each time
    
    return orig_doc, new_doc


def gng_upload(orig_doc, new_doc, new_doc_headers):
    '''Uses the csv library to write to a file for upload to REDCAP.
    Requires user to enter participant ID one at a time. Exits while loop when finished.
    PARAM: list of original PVT document entries, new document to write to,
        list of headers for REDCAP upload
    RETURN: none as of currently'''
    pvt_writer = csv.writer(new_doc, delimiter=',') #, quotechar='"', quoting=csv.QUOTE_MINIMAL
    pvt_writer.writerow(new_doc_headers) # writes the headers for uploading

    more_ptp = 'yes'
    while (more_ptp.lower() == 'yes'):
        new_ptp = input('Enter the participant ID you would like uploaded: ')
        for i in range(1, len(orig_doc)):
            row = orig_doc[i].split(',')
            if (row[1] == new_ptp):
                new_row = [row[1]+'--1', row[3], row[4], row[5], row[6].strip('\n'), 2]
                new_row2 = [row[1]+'--2', row[3], row[4], row[5], row[6].strip('\n'), 2]
                pvt_writer.writerow(new_row)
                pvt_writer.writerow(new_row2)
        more_ptp = input('More participants (yes/no)? ')
        
    print('Upload the file called \'GNG_entries.csv\' located directly inside the ' +
          '\'Organized by assessment\' folder to REDCAP.')


def run_pai():
    '''This takes a file name and attempts opening it.'''
    ##Note: current file doesn't have 106 entries, but
    ##may be faulty.
    pai_file = input('Enter the name of the PAI file (include .txt): ')
    total_pai_entries = 106
    try:
        file_content = open(pai_file).readlines()
    except:
        print('File not found. Please try again.')

    return file_content


def org_pai(file_content):
    '''Two lists removing unnecessary data are created, one being
    the headers in proper format, and one being the numerical data.
    PARAM: list of file content
    RETURN: two lists'''
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

def pai_upload(fixed_headers, fixed_entries):
    '''Opens a new CSV file and writes the row of headers as well as
    the row of data for one participant.
    PARAM: list of headers, list of entries
    RETURN: none'''
    with open('PAI_entries.csv', mode='w') as csvfile:
        pai_writer = csv.writer(csvfile, delimiter=',')
        pai_writer.writerow(fixed_headers)
        pai_writer.writerow(fixed_entries)

    csvfile.close()

def check_pai_template(fixed_headers):
    ##Temp fxn
    '''Prints which headers are part of the PAI upload but are not
    included in the text file.'''
    with open('TBIModel_ImportTemplate.csv', mode='r') as csvfile:
        pai_reader = csv.reader(csvfile, delimiter=',')
        all_headers = []
        for row in pai_reader:
            all_headers = row

    csvfile.close()

    pai_headers = []
    found = False
    for header in all_headers:
        if (header == 'icn_rawscore'):
            found = True
        elif (header == 'pai_report_complete'):
            found = False
        if (found == True):
            pai_headers.append(header)

    for template_header in pai_headers:
        if (template_header not in fixed_headers):
            print(template_header)

main()
