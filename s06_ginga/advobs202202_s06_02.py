#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/24 15:39:38 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing astroquery module
import astroquery.simbad
import astroquery.ipac.ned

# constructing parser object
desc   = "getting coordinate from given target name"
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_resolver = ['simbad', 'ned']
parser.add_argument ('-r', '--resolver', choices=choices_resolver, \
                     default='simbad', help='choice of name resolver')
parser.add_argument ('-t', '--target', default='', help='target name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
name_resolver = args.resolver
target_name   = args.target

# checking target name
if (target_name == ''):
    # printing error message
    print ("No target name is given!")
    # exit
    sys.exit ()
    
# using name resolver
if (name_resolver == 'simbad'):
    query_result = astroquery.simbad.Simbad.query_object (target_name)
elif (name_resolver == 'ned'):
    query_result = astroquery.ipac.ned.Ned.query_object (target_name)

# RA and Dec
RA  = query_result['RA'][0]
Dec = query_result['DEC'][0]

# printing result of the query
print ("%s" % target_name)
if (name_resolver == 'simbad'):
    print ("  RA  = %s (in hhmmss)" % RA)
    print ("  Dec = %s (in ddmmss)" % Dec)
elif (name_resolver == 'ned'):
    print ("  RA  = %s (in deg)" % RA)
    print ("  Dec = %s (in deg)" % Dec)
