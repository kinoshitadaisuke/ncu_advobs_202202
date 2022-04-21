#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/21 15:59:32 (CST) daisuke>
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
import astropy.io.fits
import astropy.units
import astropy.wcs

# importing photutils module
import photutils.aperture

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg
import matplotlib.patches

# constructing parser object
desc   = 'marking standard stars'
parser = argparse.ArgumentParser (description=desc)

# colour maps
choices_cmap = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', \
                'binary', 'gray', 'bone', 'pink', \
                'spring', 'summer', 'autumn', 'winter', \
                'cool', 'hot', 'copper', 'ocean', 'terrain', \
                'gnuplot', 'cubehelix', 'jet', 'turbo']

# adding command-line arguments
parser.add_argument ('-c', '--cmap', default='bone', choices=choices_cmap, \
                     help='choice of colour map (default: bone)')
parser.add_argument ('-d', '--resolution', type=int, default=450, \
                     help='resolution in DPI (default: 450)')
parser.add_argument ('-r', '--radius', type=float, default=20.0, \
                     help='radius of aperture circle in arcsec')
parser.add_argument ('-w', '--width', type=float, default=2.0, \
                     help='width of circle')
parser.add_argument ('-s', '--std', default='', help='standard star file')
parser.add_argument ('-o', '--output', default='', \
                     help='output image file name')
parser.add_argument ('file', default='', help='input FITS file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
cmap          = args.cmap
resolution    = args.resolution
radius_arcsec = args.radius
width         = args.width
file_std      = args.std
file_output   = args.output
file_fits     = args.file

# making pathlib objects
path_fits   = pathlib.Path (file_fits)
path_std    = pathlib.Path (file_std)
path_output = pathlib.Path (file_output)

# checking input FITS file
if (file_fits == ''):
    # printing message
    print ("You need to specify input file name.")
    # exit
    sys.exit ()
if not (path_fits.suffix == '.fits'):
    # printing message
    print ("Input file must be a FITS file.")
    # exit
    sys.exit ()
if not (path_fits.suffix == '.fits'):
    # printing message
    print ("Input file must be a FITS file.")
    # exit
    sys.exit ()

# checking standard star
if (file_std == ''):
    # printing message
    print ("You need to specify input file name.")
    # exit
    sys.exit ()
if not (path_std.exists ()):
    # printing message
    print ("Input standard star file '%s' does not exist." % file_std)
    # exit
    sys.exit ()
    
# checking output image file
if not ( (path_output.suffix == '.eps') or (path_output.suffix == '.pdf') \
         or (path_output.suffix == '.png') or (path_output.suffix == '.ps') ):
    # printing message
    print ("Output file must be either EPS, PDF, PNG, or PS.")
    # exit
    sys.exit ()
if (path_output.exists ()):
    # printing message
    print ("Output image file '%s' exists." % file_output)
    # exit
    sys.exit ()
    
# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # reading FITS header
    header = hdu_list[0].header

    # reading WCS information from header
    wcs = astropy.wcs.WCS (header)

    # reading FITS image data
    data = hdu_list[0].data

# making empty list
list_coords = []

# opening standard star file
with open (file_std, 'r') as fh:
    # reading file line-by-line
    for line in fh:
        # skip if the line stars with '#'
        if (line[0] == '#'):
            continue
        # splitting data
        records = line.split ()
        # RA
        ra_deg = float (records[1])
        # Dec
        dec_deg = float (records[2])
        # RA and Dec
        coord = astropy.coordinates.SkyCoord (ra_deg, dec_deg, unit='deg')
        # appending coord to list_coords
        list_coords.append (coord)

# radius of circle in pixel
pix_scale    = abs (header['CDELT1']) * 3600.0
radius_pixel = radius_arcsec / pix_scale

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

# plotting locations of standard stars
for coord in list_coords:
    # conversion from world coordinate (RA, Dec) into pixel coordinate (x, y)
    (x, y) = wcs.world_to_pixel (coord)
    # making a circle
    stdstars = matplotlib.patches.Circle (xy=(x, y), \
                                          radius=radius_pixel, \
                                          fill=False, color="red", \
                                          linewidth=width)
    # plotting location of standard star
    ax.add_patch (stdstars)

# saving file
fig.savefig (file_output, dpi=resolution)
