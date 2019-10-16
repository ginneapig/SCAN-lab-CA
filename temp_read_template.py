import csv

def check_pai_template():
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

    print(pai_headers, len(pai_headers))
main()
