# RastLeak

Tool to automatic leak information using Hacking with engine searches

# How to install

<pre> git clone https://github.com/n4xh4ck5/RastLeak.git </pre>

Install dependencies with pip:

<pre> pip install -r requirements.txt </pre>

# Usage

python rastleak.py

The last stable version is rastleak.py

$python rastleak.py -h


usage: rastleak.py [-h] -d DOMAIN -o OPTION -n SEARCH -e EXT [-f EXPORT]


This script searchs files indexed in the main searches of a domain to detect a possible leak information


optional arguments:


  -h, --help            show this help message and exit
  
  
  -d DOMAIN, --domain DOMAIN
 
  
                        The domain which it wants to search
                        
  -o OPTION, --option OPTION
  
                        Indicate the option of search
                        
                        	1.Searching leak information into the target
                          
                        	2.Searching leak information outside target
                          
  -n SEARCH, --search SEARCH
  
                        Indicate the number of the search which you want to do
                        
  -e EXT, --ext EXT     Indicate the option of display:
 
                        	1-Searching the domains where these files are found
                          
                        	2-Searching ofimatic files
                        
  -f EXPORT, --export EXPORT
  
                        Indicate the type of format to export results.
                        
                        	1.json (by default)
                          
                        	2.xlsx       
                          
# Author

Ignacio Brihuega Rodríguez aka n4xh4ck5

Twitter: @Nachoo_91

Web: fwhibbit.es

# Disclamer

The use of this tool is your responsability. I hereby disclaim any responsibility for actions taken with this tool.                          
                                                  
