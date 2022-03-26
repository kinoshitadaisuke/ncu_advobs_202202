#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/24 15:46:36 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing astroquery module
import astroquery.simbad
import astroquery.ipac.ned

# importing astropy module
import astropy.coordinates
import astropy.units

# units
u_ha  = astropy.units.hourangle
u_deg = astropy.units.deg

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

# coordinate
if (name_resolver == 'simbad'):
    coord = astropy.coordinates.SkyCoord (RA, Dec, unit=(u_ha, u_deg))
elif (name_resolver == 'ned'):
    coord = astropy.coordinates.SkyCoord (RA, Dec, unit=(u_deg, u_deg))

# coordinates in (hhmmss, ddmmss) format and (deg, deg) format
coord_str = coord.to_string (style='hmsdms')
(coord_ra_str, coord_dec_str) = coord_str.split ()
coord_ra_deg  = coord.ra.deg
coord_dec_deg = coord.dec.deg
    
# printing coordinate
print ("Target Name: %s" % target_name)
print ("  RA:  %s = %f deg" % (coord_ra_str, coord_ra_deg) )
print ("  Dec: %s = %f deg" % (coord_dec_str, coord_dec_deg) )
