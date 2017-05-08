# RastLeak
Tool to automatic leak information using Hacking with engine searches

# How to install

Install requirements with:

pip install -r requirements.txt

#How to use:

python rastleak.py

The last stable version is rastleak.py

$python rastleak_py -h

    usage: rastleak.py [-h] [-d DOMAIN] -n SEARCH -e EXT [-f EXPORT]


    This script searchs files indexed in the main searches of a domain to detect a possible leak information


optional arguments:

  -h, --help            
  
      show this help message and exit
  
  -d DOMAIN, --domain DOMAIN
  
                        The domain which it wants to search
                        
  -n SEARCH, --search SEARCH
  
                        Indicate the number of the search which you want to do
                        
  -e EXT, --ext EXT     Indicate the option of display:
  
                        	1-Searching the domains where these files are found
                          
                        	2-Searching ofimatic files
                        
  -f EXPORT, --export EXPORT
  
                        Indicate the type of format to export results.
                        
                        	1.json (by default)
                          
                        	2.xlsx
                          
