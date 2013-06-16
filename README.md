bsparse
======

bsparser is a python tool to parse the Burp Suite sitemaps.

Sitemaps can be base64 encoded on plain text.


Usage
-----

bsparser.py -i \<infile\> [action] [options]

#### Mandatory Arguments
    -i  --input                               Input sitemap (XML) file
    
#### Actions
    -w --wordlist <outfile>                   Generate a wordlist
    -p --pagelist <outfile>                   Generate a list of pages

#### Options
    -n --nano-backup                          Append ~ to output of pagelist (nano backup files)
    -v --verbose                              Verbose output
    -h --help                                 Display help text
