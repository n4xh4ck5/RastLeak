#!/usr/bin/python
# Written by Ignacio Brihuega Rodriguez 
import sys
import urllib2
import urllib
import httplib
import requests
import wget
import json
from urlparse import urlparse
from bs4 import BeautifulSoup
import optparse
#Analyze metadata pdf
import PyPDF2
from PyPDF2 import PdfFileReader
#Analyze metadata docx
import docx
import datetime
#Parser arguments
import argparse
from argparse import RawTextHelpFormatter
#define vars
#target = "%s" % sys.argv[1]
dork=["site:","-site:","filetype:","intitle:","intext:"]
urls = []
urls_clean = []
urls_final =[]
delete_bing=["microsoft","msn","bing"]
option = 0
#********************************************************#
#Define and design the dork

def DesignDork(option, num,file_ext):
	iteration=0
	initial=1
	count_bing=9
	try:
		while (iteration < num):
			if option == 1:
				#WAITING A DORK IN BING
				iteration = iteration +1
				if initial==1:
					print "\nSearching possible leak information...\n"
					initial = 0
					#First search in Bing
					SearchBing = "https://www.bing.com/search?q="+dork[0]+target+" ("+dork[2]+"pdf+OR+"+dork[2]+"doc)&go=Buscar"
						#+dork[3]+"doc"+dork[3]+"docx"+dork[3]+"xls"+dork[3]+"ppt"+")&go=Buscar"
					#https://www.bing.com/search?q=site%3Avodafone.es+%28filetype%3Apdf+OR+filetype%3Adoc+OR+filetype%3Adocx+OR+filetype%3Axls+OR+filetype%3Appt%29
					#SendRequest(SearchBing)
				else:
					#Bring the next Bing results - 50 in each page
					SearchBing=SearchBing + "&first="+str(count_bing)+"&FORM=PORE"
					#SearchBing = "https://www.bing.com/search?q="+dork[0]+target+" ("+dork[2]+"pdf)&go=Buscar&first="+str(count_bing)+"&FORM=PORE"
					#SearchBing = "https://www.bing.com/search?q="+dork[1]+target+"("+dork[3]+"pdf"+dork[3]+"doc"+dork[3]+"docx"+dork[3]+"xls"+dork[3]+"ppt"+")&go=Buscar&first="+str(count_bing)+"&FORM=PORE"
					count_bing=count_bing+50
					#SendRequest(SearchBing)
			if option == 2:
				iteration = iteration +1
				if initial==1:
					print "\nSearching possible leak information...\n"
					initial = 0
					#First search in Bing
					SearchBing = "https://www.bing.com/search?q="+dork[3]+"pdf"+dork[3]+"doc"+dork[3]+"docx"+dork[3]+"xls"+dork[3]+"ppt"+dork[0]+target+"&go=Buscar"
					#https://www.bing.com/search?q=ext%3Apdf+OR+ext%3Adoc+OR+ext%3Adocx+OR+ext%3Axls+OR+ext%3Appt+site%3Avodafone.es
					#SendRequest(SearchBing)
				else:
					#Bring the next Bing results - 50 in each page
					SearchBing = "https://www.bing.com/search?q="+dork[3]+"pdf"+dork[3]+"doc"+dork[3]+"docx"+dork[3]+"xls"+dork[3]+"ppt"+dork[0]+target+"&go=Buscar&first="+str(count_bing)+"&FORM=PORE"
					count_bing=count_bing+50
					#SendRequest(SearchBing)
			SendRequest(SearchBing)
	except:
		pass

#********************************************************#
#Doing the request to search
def SendRequest(dork):
	try:
		#Requests
		response=requests.get(dork,allow_redirects=True)	
	except:
		pass
	content = response.text	
	#PARSER HTML
	#normalize a called with parameters
	parser_html(option,file_ext,content)
#********************************************************#
#Definition and treatment of the parameters
def parser_html(option,type,content):
	i = 0
	if option == 2:
		soup = BeautifulSoup(content, 'html.parser')
		for link in soup.find_all('a'):
			try:
				if (urlparse(link.get('href'))!='' and urlparse(link.get('href'))[1].strip()!=''):
					#Split the url to identify differents parts	
					parse = urlparse(link.get('href'))[1].split(fraud_target)
					#Know the lenght of the url to verify if the result belongs to a main domain
					if len(parse[1])>4:
						urls.append(urlparse(link.get('href'))[1])
					
			except Exception as e:
				#print e
				pass	
	if option == 1: #searching ofcimatic files into target
		soup = BeautifulSoup(content, 'html.parser')
		for link in soup.find_all('a'):
			try:
				if (urlparse(link.get('href'))!='' and urlparse(link.get('href'))[1].strip()!=''):	
					#if file_ext == 1: #ofimatic files: pdf, doc,docx,xls,...
					if type == 1:
						urls.append(urlparse(link.get('href'))[1]) #dominio
					else: # file_ext == 2 -># Display the domains where the files are found.
						urls.append(link.get('href'))
			except Exception as e:
				#print(e)
				pass
	try:
		#Delete duplicates
		[urls_clean.append(i) for i in urls if not i in urls_clean] 
	except:
		pass
	try:
		#Delete not domains belongs to target
		for value in urls_clean:
			if (value.find(delete_bing[0])  == -1):
				if (value.find(delete_bing[1])  == -1):
					if (value.find(delete_bing[2])  == -1):
						urls_final.append(value)
	except:
		pass
####### FUNCTION DOWNLOADFILES ######
def ExportResults(data):
	with open ('output.json','w') as f:
			json.dump(data,f)
####### FUNCTION AnalyzeMetadata pdf ######
def Analyze_Metadata_pdf(filename):
####### FUNCTION AnalyzeMetadata ######
	pdfFile = PdfFileReader(file(filename, 'rb'))
	metadata = pdfFile.getDocumentInfo()
	print ' - Document: ' + str(filename)
	for meta in metadata:
		print ' - ' + meta + ':' + metadata[meta]
####### FUNCTION AnalyzeMetadata doc ######
def Analyze_Metadata_doc(fileName):
	#Open file
	docxFile = docx.Document(file(fileName,'rb'))
	#Get the structure
	docxInfo= docxFile.core_properties
	#Print the metadata which it wants to display
	attribute = ["author", "category", "comments", "content_status", 
	    "created", "identifier", "keywords", "language", 
	    "last_modified_by", "last_printed", "modified", 
	    "revision", "subject", "title", "version"]
	#run the list in a for loop to print the value of each metadata
	print ' - Document: ' + str(fileName)
	for meta in attribute:
	    metadata = getattr(docxInfo,meta)
	    if metadata:
	        #Separate the values unicode and time date
	        if isinstance(metadata, unicode): 
	            print " \n\t" + str(meta)+": " + str(metadata)
	            #print "\n\t",metadata
	        elif isinstance(metadata, datetime.datetime):
	            print " \n\t" + str(meta)+": " + str(metadata)
#Analyze the extension of the file to due the document:.pdf, jpg,...
#At the moment, analyze pdf's
def Analyze_Metadata(filename):
	#Verify the ext to know the type of the file to diference of the analysis
	ext=filename.lower().rsplit(".",1)[-1]
	#print ext
	if ext =="pdf":
		#call the function analyze metadata pdf
		Analyze_Metadata_pdf(filename)
	if ((ext =="doc") or (ext=="docx")):
		Analyze_Metadata_doc(filename)
####### FUNCTION DOWNLOADFILES ######
def Downloadfiles(urls_metadata):
	print "\nDo you like downloading these files to analyze metadata(Y/N)?"
	#try:
	resp = raw_input()
	if (resp == 'N'):
		print "Exiting"
		exit(1)
	if ((resp != 'Y') and (resp != 'N')):
		print "The option is not valided. Please, try again it"
	if (resp =='Y'):
		try:
			for url in urls_metadata:
				try:
					filename= wget.download(url,"/opt/")
						#+"-o /opt/file_downloaded.pdf")
					Analyze_Metadata(filename)
				except Exception, e:
					print e
		except:
			pass
#********************************************************#
#Definition and treatment of the parameters
def ShowResults(newlist,option,num_files,target):
	if option == 1:
		print "Files in the target "+target+" are:\n"
		print "Files indexed:", len (urls_final)
		for i in urls_final:
			if i not in newlist:
				newlist.append(i)
				print i		
		#verify if the user wants to export results
		if output == 'Y':
			#Only it can enter if -j is put in the execution
			ExportResults(newlist)
		#Call to function to download the files		
		Downloadfiles(newlist)
	if option == 2:
		print "Files outside target "+fraud_target+" are:\n"
		for i in urls_final:
			if i not in newlist:
				newlist.append(i)
				print i	
#INICIO MAIN
parser = argparse.ArgumentParser(description='This script searchs files indexed in the main searches of a domain to detect a possible leak information', formatter_class=RawTextHelpFormatter)
parser.add_argument('-d','--domain', help="The domain which it wants to search",required=False)
#parser.add_argument('-t','--thread', help='Indicate the number of threads to use for the enumeration\n\n',required=False)
parser.add_argument('-n','--search', help="Indicate the number of the search which you want to do",required=True)
parser.add_argument('-e','--ext', help='Indicate the option of display:\n\t1-Searching the domains where these files are found\n\t2-Searching ofimatic files\n\n', required=True)
parser.add_argument('-o','--option', help="Indicate the option of search:\n\t1- Searching leak information in the target.\n\t2 - Searching leak information outside target.",required=True)
parser.add_argument('-f','--export', help='Export the results to a json file (Y/N)\n\n',required=False)
args = parser.parse_args()
print " _____           _   _                _    "
print " |  __ \         | | | |              | |   "
print"  | |__) |__ _ ___| |_| |     ___  __ _| | __"
print"  |  _  // _` / __| __| |    / _ \/ _` | |/ /"
print"  | | \ \ (_| \__ \ |_| |___|  __/ (_| |   < "
print"  |_|  \_\__,_|___/\__|______\___|\__,_|_|\_\""
print "\nAuthor:Ignacio Brihuega\n"
#Asignation from arguments to variables.
#convertion to int the argument
num_files=0
N = int (args.search)
target=args.domain
file_ext= int(args.ext)
output=args.export
if ((output != 'Y') and (output != 'N')):
	print "The output option is not valid"
	exit(1)
option = int (args.option)
if option == 2:
	fraud_target= args.fraud_target
if (option != 1) and (option != 2):
	print "The option is not valid"
	exit(1)
#Call design the dork
try:
	num_files = DesignDork(option,N,file_ext)
except: 
	pass
newlist=[]
#Called the function to display the results
ShowResults(newlist,option,num_files,target)