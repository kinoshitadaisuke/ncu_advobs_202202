#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 13:47:37 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing re module
import re

# importing pathlib module
import pathlib

# importing ssl module
import ssl

# importing urllib module
import urllib.request

# setting for SSL
ssl._create_default_https_context = ssl._create_unverified_context

# construction of parser object
desc = 'WWW fetch'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('URL', default='', help='URL of the resource')
parser.add_argument ('-o', '--output', default='', help='output file name')
parser.add_argument ('-v', '--verbose', action="store_true", \
                     help='output file name')

# command-line argument analysis
args = parser.parse_args ()

# parameters
target_url  = args.URL
file_output = args.output
verbosity   = args.verbose

#
# check of URL
#
# making a pattern for matching by regular expression
pattern_http = re.compile ('^http')
# matching by regular expression
match_http   = re.search (pattern_http, target_url)
# if not matching, then stop the script
if not (match_http):
    # printing message
    print ("URL has to start with \"http\"!")
    print ("Check the URL!")
    print ("Stopping the script...")
    # exiting the script
    sys.exit ()

# output file name
if (file_output == ''):
    # default output file name
    #   for URL of https://aaa.bbb.ccc/ddd/eee/fff.ggg
    #   output file name ==> fff.ggg
    file_output = target_url.split ('/') [-1]

# existence check of output file
path_output = pathlib.Path (file_output)
if (path_output.exists ()):
    # printing message
    print ("The output file \"%s\" exists!" % file_output)
    print ("Stopping the script...")
    # exiting the script
    sys.exit ()

# printing input parameters
if (verbosity):
    print ("#")
    print ("# input parameters")
    print ("#  target URL  = %s" % target_url)
    print ("#  output file = %s" % file_output)
    print ("#")
    
# making a request object
req = urllib.request.Request (url=target_url)

# printing status
if (verbosity):
    print ("# now fetching the object...")

# retrieval of target
with urllib.request.urlopen (req) as www:
    # target file size
    file_size_byte = int (www.length)
    # printing file size of target
    if (verbosity):
        print ("#  file size = %10d byte" % (file_size_byte) )
        print ("#            = %10d kB" % (file_size_byte / 1024) )
        print ("#            = %10d MB" % (file_size_byte / 1024 / 1024) )
    # retrieving data
    target_data = www.read ()

# printing status
if (verbosity):
    print ("# finished fetching the object!")

# printing status
if (verbosity):
    print ("# now writing data into file...")

# opening output file for binary writing mode
with open (file_output, 'wb') as fh:
    # writing data into output file
    fh.write (target_data)

# printing status
if (verbosity):
    print ("# finished writing data into file!")
