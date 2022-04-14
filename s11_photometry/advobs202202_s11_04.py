#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/14 13:33:21 (CST) daisuke>
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
import astropy.modeling

# importing photutils module
import photutils.centroids
import photutils.aperture

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg
import matplotlib.patches

# constructing parser object
desc   = 'Setting an aperture'
parser = argparse.ArgumentParser (description=desc)

# colour maps
choices_cmap = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', \
                'binary', 'gray', 'bone', 'pink', \
                'spring', 'summer', 'autumn', 'winter', \
                'cool', 'hot', 'copper', 'ocean', 'terrain', \
                'gnuplot', 'cubehelix', 'jet', 'turbo']

# adding command-line arguments
parser.add_argument ('-f', '--fwhm', type=float, default=4.0, \
                     help='FWHM of stellar PSF in pixel (default: 4.0)')
parser.add_argument ('-a', '--aperture', type=float, default=1.5, \
                     help='aperture radius in FWHM (default: 1.5)')
parser.add_argument ('-w', '--width', type=int, default=15, \
                     help='half-width of subframe to be plotted (default: 15)')
parser.add_argument ('-x', '--xcentre', type=float, default=-1, \
                     help='x coordinate of target')
parser.add_argument ('-y', '--ycentre', type=float, default=-1, \
                     help='y coordinate of target')
parser.add_argument ('-r', '--resolution', type=int, default=450, \
                     help='resolution in DPI (default: 450)')
parser.add_argument ('-m', '--cmap', default='bone', choices=choices_cmap, \
                     help='choice of colour map (default: bone)')
parser.add_argument ('-o', '--output', default='', \
                     help='output file name')
parser.add_argument ('file', default='', help='input file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
fwhm_pixel           = args.fwhm
aperture_radius_fwhm = args.aperture
half_width           = args.width
x_centre             = args.xcentre
y_centre             = args.ycentre
resolution           = args.resolution
cmap                 = args.cmap
file_output          = args.output
file_fits            = args.file

# aperture radius in pixel
aperture_radius_pixel = aperture_radius_fwhm * fwhm_pixel

# making pathlib objects
path_fits   = pathlib.Path (file_fits)
path_output = pathlib.Path (file_output)

# checking input FITS file name
if (file_fits == ''):
    # printing message
    print ("You need to specify input file name.")
    # exit
    sys.exit ()
# if input file is not a FITS file, then stop the script
if not (path_fits.suffix == '.fits'):
    # printing message
    print ("Input file must be a FITS file.")
    # exit
    sys.exit ()
# if input file does not exist, then stop the script
if not (path_fits.exists ()):
    # printing message
    print ("Input file does not exist.")
    # exit
    sys.exit ()
# if output file exists, then stop the script
if (path_output.exists ()):
    # printing message
    print ("Output file exists.")
    # exit
    sys.exit ()
# output file must be either EPS, PDF, PNG, or PS file
if not ( (path_output.suffix == '.eps') or (path_output.suffix == '.pdf') \
         or (path_output.suffix == '.png') or (path_output.suffix == '.ps') ):
    # printing message
    print ("Output file must be either EPS, PDF, PNG, or PS file.")
    # exit
    sys.exit ()

# printing status
print ("# now, reading FITS file '%s'..." % file_fits)
    
# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # reading FITS header
    header = hdu_list[0].header

    # image size
    image_size_x = header['NAXIS1']
    image_size_y = header['NAXIS2']
    
    # checking x_centre and y_centre
    if not ( (x_centre >=0) and (x_centre < image_size_x) ):
        # printing message
        print ("Input x_centre value exceed image size.")
        # exit
        sys.exit ()
    if not ( (y_centre >=0) and (y_centre < image_size_y) ):
        print ("Input y_centre value exceed image size.")
        # printing message
        sys.exit ()
        # exit
    
    # reading FITS image data
    data = hdu_list[0].data

# printing status
print ("# finished reading FITS file '%s'!" % file_fits)

# printing status
print ("# now, generating an aperture...")
    
# making subframe
x_min = int (x_centre) - half_width
x_max = int (x_centre) + half_width + 1
y_min = int (y_centre) - half_width
y_max = int (y_centre) + half_width + 1
subframe = data[y_min:y_max, x_min:x_max]

# calculating statistical values
subframe_median = numpy.median (subframe)
subframe_stddev = numpy.std (subframe)

# position of the centre on subframe
x_centre_sub = x_centre - x_min
y_centre_sub = y_centre - y_min
position = (x_centre_sub, y_centre_sub)

# making an aperture
apphot_aperture = photutils.aperture.CircularAperture (position, \
                                                       r=aperture_radius_pixel)

# printing aperture
print (apphot_aperture)

# printing status
print ("# finished generating an aperture!")

# printing status
print ("# now, generating a plot...")

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# axes
ax.set_xlabel ('X [pixel]')
ax.set_ylabel ('Y [pixel]')

# plotting image
im = ax.imshow (subframe, origin='lower', cmap=cmap, \
                vmin=subframe_median - 3.0 * subframe_stddev, \
                vmax=subframe_median + 6.0 * subframe_stddev)
fig.colorbar (im)
ax.plot (x_centre_sub, y_centre_sub, marker='+', color='blue', markersize=10)

# adding a bar to represent FWHM
bar = matplotlib.patches.Rectangle (xy=(1,1), width=fwhm_pixel, height=1.0, \
                                    facecolor='green', edgecolor='white')
ax.add_patch (bar)

# adding a circle to represent aperture for photometry
ap = matplotlib.patches.Circle (xy=position, radius=aperture_radius_pixel, \
                                fill=False, color="yellow", linewidth=3)
ax.add_patch (ap)

# saving file
fig.savefig (file_output, dpi=resolution)

# printing status
print ("# finished generating a plot!")
