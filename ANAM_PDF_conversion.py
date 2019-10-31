# Annie Gao
# anniegao@email.arizona.edu
# Created: 10/23/2019
# Last edited: 10/25/2019

'''This program attempts to use Optical Character Recognition (OCR)
libraries to extract text information out of a PDF. This focuses on
pulling information out of ANAM.'''

from PIL import Image # uses Pillow, a fork of PIL
import pytesseract
from pdf2image import convert_from_path
import sys
import os

import csv
from collections import OrderedDict

def main():
    anam_doc = open('ANAM_entries.csv', mode='w')
    more_ptp = 'yes'
    headers_written = False
    while(more_ptp == 'yes'):
        print('beginning', headers_written)
        new_ptp = input('Enter the participant ID you would like uploaded: ')
        #new_ptp = '100'
        #file_name = './ANAM_example' 
        file_name = input('Name of ANAM file (do not include .pdf)? ')
        pages = PDF_to_images(file_name)
        output_file = images_to_text(file_name, pages)
        
        anam_dict = OrderedDict() # for later writing rows
        anam_dict['participantid'] = new_ptp
        #output_file = 'ANAM_example.txt' ##spoofing
        organize_text(output_file, anam_dict)
        headers_written = anam_upload(anam_doc, anam_dict, headers_written)
        print(headers_written)
        more_ptp = input('More participants (yes/no)? ').lower()
    
    anam_doc.close()


def PDF_to_images(file_name):
    '''Converts the inputted PDF to an image for each
    page of the PDF.
    PARAM: string name of PDF file
    RETURN: list object of pages'''
    #PDF_file = './adfja/dasfsa/{}.pdf'.format(file_name)
    PDF_file = file_name+'.pdf' ##spoofing
    pages = convert_from_path(PDF_file, dpi=550) # dpi = dots per inch

    for i in range(0, len(pages)):
        page = pages[i]
        page_num = i+1
        file_name = 'page_{}.jpg'.format(page_num)
        page.save(file_name, 'JPEG')

    return pages

def images_to_text(file_name, pages):
    '''Converts the newly created images to one text file.
    PARAM: string name of PDF file for output file name
    RETURN: string name of output file'''
    output_file = '{}.txt'.format(file_name)
    f = open(output_file, 'w')

    for i in range(0, len(pages)):
        page_num = i+1
        file_name = 'page_{}.jpg'.format(page_num)
        text = str(pytesseract.image_to_string(Image.open(file_name)))
        os.remove(file_name) # can delete image file now that text is extracted

        # For many PDFs at a line ending, if a word can't be written fully, 
        # a '-' is added and the rest of the word is on the next line.
        # Remove this by replacing every '-\n' with ''.
        text = text.replace('-\n','') 
        f.write(text)

    f.close()
    return output_file

def sort_category(file_content, start, category, anam_dict):
    '''Helper function: locates necessary information
    in each category, based on category name.
    PARAM: list of lines from file, index of where corresponding data starts,
        string name of category, Ordered Dictionary of ANAM headers to appropriate data
    RETURN: none'''
    c_ic_l = file_content[start].split()
    anam_dict[category + '_correct'] = c_ic_l[1]
    anam_dict[category + '_incorrect'] = c_ic_l[3]
    anam_dict[category + '_lapse'] = c_ic_l[5]

    for i in range(start, len(file_content)):
        curr_line = file_content[i]
        if ('Mean RT' in curr_line):
            mean_rt = curr_line.split()
            count = 0
            for j in range(0, len(mean_rt)):
                if (mean_rt[j].isdigit()):
                    count += 1 # counts for each int found
                    if (count == 1):
                        anam_dict[category + '_meanrt_score'] = mean_rt[j]
                    elif (count == 2):
                        anam_dict[category + '_meanrt_percentile'] = mean_rt[j]
                    elif (count == 3):
                        anam_dict[category + '_meanrt_stdsc'] = mean_rt[j]
                        break

        # must include space after % in string checking
        elif ('% ' in curr_line and category != 'srt' and category != 'srtdelay'): 
            percent = curr_line.split()
            count = 0
            for j in range(0, len(percent)):
                if(percent[j].isdigit()):
                    count += 1
                    if (count == 1):
                        anam_dict[category + '_percorrect_score'] = percent[j]
                    elif (count == 2):
                        anam_dict[category + '_percorrect_percentile'] = percent[j]
                    elif (count == 3):
                        anam_dict[category + '_percorrect_stdsc'] = percent[j]
                        break
        
        elif ('Throughput' in curr_line):
            throughput = curr_line.split()
            count = 0
            for j in range(0, len(throughput)):
                if (throughput[j].isdigit()):
                    count += 1
                    if (count == 1):
                        anam_dict[category + '_thruput_score'] = throughput[j]
                    elif (count == 2):
                        anam_dict[category + '_thruput_percentile'] = throughput[j]
                    elif (count == 3):
                        anam_dict[category + '_thruput_stdsc'] = throughput[j]
                        break
            break


def organize_text(output_file, anam_dict):
    '''Opens text file and locates all data, storing
    it in a dictionary.
    PARAM: string of output file name, dictionary to hold all ANAM headers
    RETURN: none'''
    file_content = open(output_file).readlines()
    
    for i in range(0, len(file_content)):
        line1 = file_content[i]
        if ('COMPOSITE SCORE' in line1):
            for j in range(i, len(file_content)): # 2nd loop for clarity
                line2 = file_content[j]
                if ('Score' in line2): # 'Score' very ambiguous
                    colon = line2.index(':')
                    anam_dict['composite_score'] = line2[colon+1:].strip()
                    break
        
        if ('SLEEP SCALE' in line1):
            for j in range(i, len(file_content)):
                line2 = file_content[j]
                if (': ' in line2):
                    colon = line2.index(':')
                    anam_dict['sleep_scale'] = line2[colon+1:colon+3].strip()
                    break
        
        if ('SIMPLE REACTION TIME' in line1 and 'Comparison Group' not in line1):
            for j in range(i, len(file_content)):
                line2 = file_content[j]
                if ('Correct' in line2):
                    sort_category(file_content, j, 'srt', anam_dict)
                    break

        if ('CODE SUBSTITUTION' in line1 and 'LEARNING' in line1):
            for j in range(i, len(file_content)):
                line2 = file_content[j]
                if ('Correct' in line2):
                    sort_category(file_content, j, 'codesub', anam_dict)
                    break
        
        if ('PROCEDURAL REACTION TIME' in line1):
            for j in range(i, len(file_content)):
                line2 = file_content[j]
                if ('Correct' in line2):
                    sort_category(file_content, j, 'procrt', anam_dict)
                    break
        
        if ('MATHEMATICAL PROCESSING' in line1):
            for j in range(i, len(file_content)):
                line2 = file_content[j]
                if ('Correct' in line2):
                    sort_category(file_content, j, 'mathpro', anam_dict)
                    break

        if ('MATCHING TO SAMPLE' in line1):
            for j in range(i, len(file_content)):
                line2 = file_content[j]
                if ('Correct' in line2):
                    sort_category(file_content, j, 'mts', anam_dict)
                    break
        
        if ('CODE SUBSTITUTION' in line1 and 'DELAYED' in line1):
            for j in range(i, len(file_content)):
                line2 = file_content[j]
                if ('Correct' in line2):
                    sort_category(file_content, j, 'csdelay', anam_dict)
                    break

        if ('SIMPLE REACTION TIME' in line1 and 'Comparison Group' in line1):
            for j in range(i, len(file_content)):
                line2 = file_content[j]
                if ('Correct' in line2):
                    sort_category(file_content, j, 'srtdelay', anam_dict)
                    break
    
    anam_dict['anam_report_complete'] = 2 # complete

def anam_upload(anam_doc, anam_dict, headers_written):
    '''Takes content from the dictionary of one participant and 
    writes it into a CSV file. Will only write headers once.
    PARAM: Ordered Dictionary of one ptp's ANAM data, 
        boolean value used for writing headers
    RETURN: none'''
    anam_writer = csv.writer(anam_doc, delimiter=',')
    if (not headers_written):
        # directly turns into list with * interactor unpacking operator
        anam_writer.writerow([*anam_dict.keys()]) 

    anam_writer.writerow([*anam_dict.values()]) 

    return True

main()
