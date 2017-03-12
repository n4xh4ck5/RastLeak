#!/usr/bin/env python

import requests
import wget
import json
from urlparse import urlparse
from bs4 import BeautifulSoup
import optparse
# Analyze metadata pdf
import PyPDF2
from PyPDF2 import PdfFileReader
# Analyze metadata docx
import docx
import datetime
# Parser arguments
import argparse
from argparse import RawTextHelpFormatter
# define vars
dork = ["site:", "-site:", "filetype:", "intitle:", "intext:"]
urls = []
urls_clean = []
urls_final = []
delete_bing = ["microsoft", "msn", "bing"]
option = 0


def DesignDork(num, file_ext):
    """
    Define and design the dork
    """
    iteration = 0
    initial = 1
    count_bing = 9
    try:
        while (iteration < num):
            # WAITING A DORK IN BING
            iteration = iteration + 1
            if initial == 1:
                print "\nSearching possible leak information...\n"
                initial = 0
                # First search in Bing
                SearchBing = "https://www.bing.com/search?q=" + \
                    dork[0] + target + \
                    " (" + dork[2] + "pdf+OR+" + dork[2] + "doc)&go=Buscar"
            else:
                # Bring the next Bing results - 50 in each page
                SearchBing = SearchBing + "&first=" + \
                    str(count_bing) + "&FORM=PORE"
                count_bing = count_bing + 50
            SendRequest(SearchBing)
    except:
        pass

def SendRequest(dork):
    """
    Doing the request to search
    """
    try:
        # Requests
        response = requests.get(dork, allow_redirects=True)
    except:
        pass
    content = response.text
    # PARSER HTML
    # normalize a called with parameters
    parser_html(file_ext, content)

def parser_html(type, content):
    """
    Definition and treatment of the parameters
    """
    i = 0
    soup = BeautifulSoup(content, 'html.parser')
    for link in soup.find_all('a'):
        try:
            if (urlparse(link.get('href')) != '' and urlparse(link.get('href'))[1].strip() != ''):
                # if file_ext == 1: #ofimatic files: pdf, doc,docx,xls,...
                if type == 1:
                    urls.append(urlparse(link.get('href'))[1])  # dominio
                # file_ext == 2 -># Display the domains where the files are
                # found.
                else:
                    urls.append(link.get('href'))
        except Exception as e:
            # print(e)
            pass
    try:
        # Delete duplicates
        [urls_clean.append(i) for i in urls if not i in urls_clean]
    except:
        pass
    try:
        # Delete not domains belongs to target
        for value in urls_clean:
            if (value.find(delete_bing[0]) == -1):
                if (value.find(delete_bing[1]) == -1):
                    if (value.find(delete_bing[2]) == -1):
                        urls_final.append(value)
    except:
        pass


def ExportResults(data):
    """
    FUNCTION DOWNLOADFILES
    """
    with open('output.json', 'w') as f:
        json.dump(data, f)

def Analyze_Metadata_pdf(filename):
    """
    FUNCTION AnalyzeMetadata pdf
    """
    pdfFile = PdfFileReader(file(filename, 'rb'))
    metadata = pdfFile.getDocumentInfo()
    print ' - Document: ' + str(filename)
    for meta in metadata:
        print ' - ' + meta + ':' + metadata[meta]

def Analyze_Metadata_doc(fileName):
    """
    FUNCTION AnalyzeMetadata doc
    """
    # Open file
    docxFile = docx.Document(file(fileName, 'rb'))
    # Get the structure
    docxInfo = docxFile.core_properties
    # Print the metadata which it wants to display
    attribute = ["author", "category", "comments", "content_status",
                 "created", "identifier", "keywords", "language",
                 "last_modified_by", "last_printed", "modified",
                 "revision", "subject", "title", "version"]
    # run the list in a for loop to print the value of each metadata
    print ' - Document: ' + str(fileName)
    for meta in attribute:
        metadata = getattr(docxInfo, meta)
        if metadata:
            # Separate the values unicode and time date
            if isinstance(metadata, unicode):
                print " \n\t" + str(meta) + ": " + str(metadata)
            elif isinstance(metadata, datetime.datetime):
                print " \n\t" + str(meta) + ": " + str(metadata)


def Analyze_Metadata(filename):
    # Verify the ext to know the type of the file to diference of the analysis
    ext = filename.lower().rsplit(".", 1)[-1]
    # print ext
    if ext == "pdf":
            # call the function analyze metadata pdf
        Analyze_Metadata_pdf(filename)
    if ((ext == "doc") or (ext == "docx")):
        Analyze_Metadata_doc(filename)


def Downloadfiles(urls_metadata):
    """
    FUNCTION DOWNLOADFILES
    """
    print "\nDo you like downloading these files to analyze metadata(Y/N)?"
    # try:
    resp = raw_input()
    resp.upper()
    if (resp == 'N'):
        print "Exiting"
        exit(1)
    if ((resp != 'Y') and (resp != 'N')):
        print "The option is not valided. Please, try again it"
    if (resp == 'Y'):
        try:
            for url in urls_metadata:
                try:
                    filename = wget.download(url, "/opt/")
                    Analyze_Metadata(filename)
                except Exception, e:
                    print e
        except:
            pass

def ShowResults(newlist, num_files, target):
    """
    Definition and treatment of the parameters
    """
    print "Files in the target " + target + " are:\n"
    print "Files indexed:", len(urls_final)
    for i in urls_final:
        if i not in newlist:
            newlist.append(i)
            print i
    # verify if the user wants to export results
    if output == 'Y':
        # Only it can enter if -j is put in the execution
        ExportResults(newlist)
    # Call to function to download the files
    Downloadfiles(newlist)

# INICIO MAIN
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This script searches files indexed in the main searches of a domain to detect a possible leak information', formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '-d', '--domain', help="The domain which it wants to search", default='')
    parser.add_argument(
        '-n', '--search', help="Indicate the number of the search which you want to do", required=True)
    parser.add_argument(
        '-e', '--ext', help='Indicate the option of display:\n\t1-Searching the domains where these files are found\n\t2-Searching ofimatic files\n\n', required=True)
    parser.add_argument(
        '-f', '--export', help='Export the results to a json file (Y/N)\n\n', default='N')
    args = parser.parse_args()
    print " _____           _   _                _    "
    print " |  __ \         | | | |              | |   "
    print"  | |__) |__ _ ___| |_| |     ___  __ _| | __"
    print"  |  _  // _` / __| __| |    / _ \/ _` | |/ /"
    print"  | | \ \ (_| \__ \ |_| |___|  __/ (_| |   < "
    print"  |_|  \_\__,_|___/\__|______\___|\__,_|_|\_\""
    print """
    ** Tool to automatic leak information using Bing Hacking
    ** Version 1.0
    ** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
    ** DISCLAMER This tool was developed for educational purposes. 
    ** The authors are not responsible for using to others purposes.
    ** A high power, carries a high responsibility!
    """
    num_files = 0
    N = int(args.search)
    target = args.domain
    file_ext = int(args.ext)
    output = args.export
    if ((output != 'Y') and (output != 'N')):
        print "The output option is not valid"
        exit(1)
    # Call design the dork
    try:
        num_files = DesignDork(N, file_ext)
    except:
        pass
    newlist = []
    # Called the function to display the results
    ShowResults(newlist, num_files, target)
    
