#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/28 12:02:45 (CST) daisuke>
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

# importing photutils module
import photutils.aperture

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg
import matplotlib.patches

# constructing parser object
desc   = 'marking target object'
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
parser.add_argument ('-r', '--ra', type=float, default=-999.999, \
                     help='RA in degree')
parser.add_argument ('-d', '--dec', type=float, default=-999.999, \
                     help='Dec in degree')
parser.add_argument ('-s', '--size', type=float, default=10.0, \
                     help='radius of aperture in arcsec (default: 10)')
parser.add_argument ('-w', '--width', type=float, default=2.0, \
                     help='width of circle (default: 2)')
parser.add_argument ('-l', '--resolution', type=int, default=450, \
                     help='resolution of output image in DPI (default: 450)')
parser.add_argument ('-c', '--cmap', default='bone', choices=choices_cmap, \
                     help='choice of colour map (default: bone)')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_fits      = args.input
file_output    = args.output
target_ra_deg  = args.ra
target_dec_deg = args.dec
radius_arcsec  = args.size
width          = args.width
resolution     = args.resolution
cmap           = args.cmap

# check of RA and Dec
if ( (target_ra_deg < 0.0) or (target_ra_deg > 360.0) \
     or (target_dec_deg < -90.0) or (target_dec_deg > 90.0) ):
    # printing message
    print ("Something is wrong with RA or Dec!")
    print ("Check RA and Dec you specify.")
    print ("RA  = %f deg" % target_ra_deg)
    print ("Dec = %f deg" % target_dec_deg)
    # exit
    sys.exit ()

# making pathlib objects
path_fits   = pathlib.Path (file_fits)
path_output = pathlib.Path (file_output)

# existence checks
if not (path_fits.exists ()):
    # printing message
    print ("The file \"%s\" does not exist!")
    # exit
    sys.exit ()
if (path_output.exists ()):
    # printing message
    print ("The file \"%s\" exists!")
    # exit
    sys.exit ()

# check of FITS file name
if not (path_fits.suffix == '.fits'):
    # printing message
    print ("The file \"%s\" is not a FITS file!" % file_fits)
    print ("Check the file name.")
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
    
# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # reading header information
    header = hdu_list[0].header
    # WCS information
    wcs = astropy.wcs.WCS (header)
    # reading image data
    data   = hdu_list[0].data

# coordinate of standard star in RA and Dec
coord = astropy.coordinates.SkyCoord (target_ra_deg, target_dec_deg, unit='deg')

# conversion into hmsdms format
radec_str = coord.to_string ('hmsdms')
(ra_str, dec_str) = radec_str.split ()

# (x, y) coordinate of standard star on image
(x, y) = wcs.world_to_pixel (coord)

# printing (RA, Dec) and (x, y) of standard star
print ("(RA, Dec) = (%s, %s)" % (ra_str, dec_str) )
print ("(x, y)    = (%f, %f)" % (x, y) )

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

# making a circle to indicate the location of standard star
stdstars = matplotlib.patches.Circle (xy=(x, y), radius=radius_pixel, \
                                      fill=False, color="red", linewidth=width)
# plotting location of standard star
ax.add_patch (stdstars)

# invert Y-axis
ax.invert_yaxis ()

# saving file
fig.savefig (file_output, dpi=resolution)
