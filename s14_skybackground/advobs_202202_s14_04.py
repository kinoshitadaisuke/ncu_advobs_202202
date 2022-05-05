#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/05/05 12:39:26 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing numpy module
import numpy

# importing astropy module
import astropy.coordinates
import astropy.units
import astropy.wcs

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# constructing parser object
desc   = 'marking target objects'
parser = argparse.ArgumentParser (description=desc)

# colour maps
choices_cmap = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', \
                'binary', 'gray', 'bone', 'pink', \
                'spring', 'summer', 'autumn', 'winter', \
                'cool', 'hot', 'copper', 'ocean', 'terrain', \
                'gnuplot', 'cubehelix', 'jet', 'turbo']

# adding argument
parser.add_argument ('-i', '--input', default='', \
                     help='input FITS file name')
parser.add_argument ('-o', '--output', default='', \
                     help='output image file name')
parser.add_argument ('-c', '--catalogue', default='', \
                     help='standard star catalogue file name')
parser.add_argument ('-r', '--radius', type=float, default=10.0, \
                     help='radius of aperture in pixel (default: 10)')
parser.add_argument ('-w', '--width', type=float, default=2.0, \
                     help='width of circle (default: 2)')
parser.add_argument ('-l', '--resolution', type=int, default=450, \
                     help='resolution of output image in DPI (default: 450)')
parser.add_argument ('-m', '--cmap', default='bone', choices=choices_cmap, \
                     help='choice of colour map (default: bone)')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_cat    = args.catalogue
file_fits   = args.input
file_output = args.output
radius_pix  = args.radius
width       = args.width
resolution  = args.resolution
cmap        = args.cmap

# making pathlib objects
path_cat    = pathlib.Path (file_cat)
path_fits   = pathlib.Path (file_fits)
path_output = pathlib.Path (file_output)

# if output file name is not given, then stop the script
if (file_output == ''):
    # printing message
    print ("ERROR: output file name has to be given.")
    # exit
    sys.exit ()

# existence checks of files
if not (path_cat.exists ()):
    # printing message
    print ("ERROR: the file '%s' does not exist!" % file_cat)
    # exit
    sys.exit ()
if not (path_fits.exists ()):
    # printing message
    print ("ERROR: the file '%s' does not exist!" % file_fits)
    # exit
    sys.exit ()
if (path_output.exists ()):
    # printing message
    print ("ERROR: the file '%s' exists!" % file_output)
    # exit
    sys.exit ()

# check of FITS file name
if not (path_fits.suffix == '.fits'):
    # printing message
    print ("ERROR: The file \"%s\" is not a FITS file!" % file_fits)
    print ("ERROR: Check the file name.")
    # exit
    sys.exit ()

# check of output image file
if not ( (path_output.suffix == '.eps') or (path_output.suffix == '.pdf') \
         or (path_output.suffix == '.png') or (path_output.suffix == '.ps') ):
    # printing message
    print ("Output image file must be either EPS, PDF, PNG, or PS.")
    print ("Given output image file name = %s" % file_output)
    # exit
    sys.exit ()

# check of catalogue file
if not ( (path_cat.suffixes[0] == '.txt') \
         and (path_cat.suffixes[1] == '.clean') \
         and (path_cat.suffixes[2] == '.v3') ):
    # printing message
    print ("ERROR: Catalogue file must be SDSS standard star catalogue.")
    print ("ERROR: Given catalogue file name = %s" % file_cat)
    # exit
    sys.exit ()

# making an empty dictionary to store data for standards
dic_stds = {}

# opening catalogue file
with open (file_cat, 'r') as fh:
    # reading the file line-by-line
    for line in fh:
        # if the line stars with '#', then skip
        if (line[0] == '#'):
            continue
        # splitting the data
        records = line.split ()
        # star ID
        star_id = int (records[0])
        # RA
        ra_deg  = float (records[1])
        # Dec
        dec_deg = float (records[2])
        # adding data to the dictionary
        if not (star_id in dic_stds):
            dic_stds[star_id] = {}
            dic_stds[star_id]['RA_deg'] = ra_deg
            dic_stds[star_id]['Dec_deg'] = dec_deg

# positions of standard stars
positions = []
for star in dic_stds.keys ():
    positions.append ( (dic_stds[star]['RA_deg'], dic_stds[star]['Dec_deg']) )

# making Astropy's coordinate object
coords = astropy.coordinates.SkyCoord (positions, unit='deg')

# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # reading header information
    header = hdu_list[0].header
    # WCS information
    wcs = astropy.wcs.WCS (header)
    # reading image data
    data   = hdu_list[0].data

# (x, y) coordinate of standard star on image
(x, y) = wcs.world_to_pixel (coords)

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111, projection=wcs)

# axes
ax.set_xlabel ('RA')
ax.set_ylabel ('Dec')

# plotting image
norm \
    = astropy.visualization.mpl_normalize.ImageNormalize \
    ( stretch=astropy.visualization.HistEqStretch (data) )
im = ax.imshow (data, origin='lower', cmap=cmap, norm=norm)
fig.colorbar (im)

# plotting each standard star location
for i in range ( len (x) ):
    # making a circle to indicate the location of standard star
    stdstars = matplotlib.patches.Circle (xy=(x[i], y[i]), \
                                          radius=radius_pix, \
                                          fill=False, color="red", \
                                          linewidth=width)
    # plotting location of standard star
    ax.add_patch (stdstars)

# invert Y-axis
ax.invert_yaxis ()

# saving file
fig.savefig (file_output, dpi=resolution)
