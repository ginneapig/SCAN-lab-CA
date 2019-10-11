'''
# Annie Gao
# Created: 10/10/2019
# Last edited: 10/10/2019

This program's purpose is to upload ANAM and PAI files,
both usually in PDF format, to REDCap for the TBI Model arm
of the SCAN lab.'''



import CSV

def main():
    pai_file = 'TBI_999.txt'
    org_pai(pai_file)





def org_pai(pai_file):
    try:
        file_content = open(pai_file).readlines()
    except:
        print('File not found.')

    headers = file_content[0].split(',')
    entries = file_content[0].split(',')

    pai_dict = {}
    for i in range(len(headers)):
        pai_dict[headers[i]] = entries[i]

    

main()