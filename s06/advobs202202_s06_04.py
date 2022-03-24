#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/24 16:36:53 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astroquery module
import astroquery.simbad
import astroquery.ipac.ned
import astroquery.skyview

# importing astropy module
import astropy.coordinates
import astropy.units

# importing datetime module
import datetime

# importing ssl module
import ssl

# allow insecure downloading
ssl._create_default_https_context = ssl._create_unverified_context

# date/time
now = datetime.datetime.now ().isoformat ()

# units
u_ha  = astropy.units.hourangle
u_deg = astropy.units.deg

# constructing parser object
desc   = "getting coordinate from given target name"
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_resolver = ['simbad', 'ned']
choices_survey   = ['DSS1 Blue', 'DSS1 Red', 'DSS2 Blue', \
                    'DSS2 Red', 'DSS2 IR', \
                    'SDSSu', 'SDSSg', 'SDSSr', 'SDSSi', 'SDSSz']
parser.add_argument ('-r', '--resolver', choices=choices_resolver, \
                     default='simbad', help='choice of name resolver')
parser.add_argument ('-s', '--survey', choices=choices_survey, \
                     default='DSS2 Blue', help='choice of survey')
parser.add_argument ('-t', '--target', default='', help='target name')
parser.add_argument ('-f', '--fov', type=int, default=1024, \
                     help='field-of-view in pixel')
parser.add_argument ('-o', '--output', default='', help='output file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
name_resolver = args.resolver
survey        = args.survey
target_name   = args.target
fov_pix       = args.fov
file_output   = args.output

# checking target name
if (target_name == ''):
    # printing error message
    print ("No target name is given!")
    # exit
    sys.exit ()

# checking output file name
if (file_output == ''):
    # printing error message
    print ("No output file name is given!")
    # exit
    sys.exit ()
else:
    # making pathlib object
    path_fits = pathlib.Path (file_output)
    # if output file is not a FITS file, then stop the script
    if not (path_fits.suffix == '.fits'):
        # printing error message
        print ("Output file must be FITS file!")
        # exit
        sys.exit ()
    # if output file exists, then stop the script
    if (path_fits.exists ()):
        # printing error message
        print ("Output file \"%s\" exists!" % file_output)
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
print ("# Target Name: %s" % target_name)
print ("#   RA:  %s = %f deg" % (coord_ra_str, coord_ra_deg) )
print ("#   Dec: %s = %f deg" % (coord_dec_str, coord_dec_deg) )

# printing status
print ("#")
print ("# now, querying image list...")
print ("#")

# searching image
list_image = astroquery.skyview.SkyView.get_image_list (position=coord, \
                                                        survey=survey)

# printing status
print ("#")
print ("# finished querying image list!")
print ("#")

# printing image list
print ("# Available images:")
print ("# ", list_image)

# printing status
print ("#")
print ("# now, downloading image...")
print ("#")

# getting image
images = astroquery.skyview.SkyView.get_images (position=coord, \
                                                survey=survey, pixels=fov_pix)

# printing status
print ("#")
print ("# finished downloading image!")
print ("#")

# printing status
print ("#")
print ("# now, writing a FITS file...")
print ("#")

# header and data
image0  = images[0][0]
header0 = image0.header
data0   = image0.data

# adding comments in header
header0['history'] = "image downloaded from %s" % survey
header0['history'] = "image saved on %s" % now

# saving to a FITS file
astropy.io.fits.writeto (file_output, data0, header=header0)

# printing status
print ("#")
print ("# finished writing a FITS file!")
print ("#")
