#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/06/09 22:27:06 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing datetime module
import datetime

# importing numpy module
import numpy.ma

# importing astropy module
import astropy.convolution
import astropy.io.fits
import astropy.stats
import astropy.visualization
import astropy.visualization.mpl_normalize

# importing photutils module
import photutils.segmentation

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# date/time
now = datetime.datetime.now ()

# constructing parser object
desc   = 'source extraction using image segmentation and deblending'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-i', '--file-input', default='', \
                     help='input FITS file name')
parser.add_argument ('-o', '--file-catalogue', default='', \
                     help='output catalogue file name')
parser.add_argument ('-g', '--file-fig', default='', \
                     help='output figure file name')
parser.add_argument ('-t', '--threshold', type=float, default=3.0, \
                     help='detection threshold in sigma (default: 3)')
parser.add_argument ('-u', '--threshold-for-sky', type=float, default=2.0, \
                     help='detection threshold for sky estimate (default: 2)')
parser.add_argument ('-n', '--npixels', type=int, default=5, \
                     help='minimum number of pixels for detection (default: 5)')
parser.add_argument ('-s', '--dilate-size', type=int, default=21, \
                     help='dilate size (default: 21)')
parser.add_argument ('-m', '--maxiters', type=int, default=30, \
                     help='maximum number of iterations (default: 30)')
parser.add_argument ('-c', '--sigma-clipping', type=float, default=4.0, \
                     help='sigma-clipping threshold in sigma (default: 4)')
parser.add_argument ('-k', '--gaussian-fwhm', type=float, default=3.0, \
                     help='Gaussian FWHM in pixel for convolution (default: 3)')
parser.add_argument ('-a', '--kernel-size', type=int, default=3, \
                     help='Gaussian kernel array size in pixel (default: 3)')
parser.add_argument ('-r', '--radius', type=float, default=30.0, \
                     help='radius of aperture in pixel (default: 30)')

# command-line argument analysis
args = parser.parse_args ()

# file names
file_input     = args.file_input
file_catalogue = args.file_catalogue
file_fig       = args.file_fig

# input parameters
threshold         = args.threshold
threshold_for_sky = args.threshold
npixels           = args.npixels
dilate_size       = args.dilate_size
maxiters          = args.maxiters
rejection         = args.sigma_clipping
gaussian_fwhm     = args.gaussian_fwhm
kernel_array_size = args.kernel_size
radius            = args.radius

# making pathlib objects
path_input     = pathlib.Path (file_input)
path_catalogue = pathlib.Path (file_catalogue)
path_fig       = pathlib.Path (file_fig)

# check of input file name
if not (path_input.suffix == '.fits'):
    # printing message
    print ("Input file must be a FITS file.")
    # exit
    sys.exit ()

# check of catalogue file name
if (file_catalogue == ''):
    # printing message
    print ("Catalogue file name must be specified.")
    # exit
    sys.exit ()

# check of figure file name
if not ( (path_fig.suffix == '.eps') or (path_fig.suffix == '.pdf') \
         or (path_fig.suffix == '.png') or (path_fig.suffix == '.ps') ):
    # printing message
    print ("Figure file name must be either EPS, PDF, PNG, or PS.")
    # exit
    sys.exit ()

# existence check of input file
if not (path_input.exists ()):
    # printing message
    print ("ERROR: Input file '%s' does not exist." % (file_input) )
    # exit
    sys.exit ()

# existence check of catalogue file
if (path_catalogue.exists ()):
    # printing message
    print ("ERROR: Catalogue file '%s' exists." % (file_catalogue) )
    # exit
    sys.exit ()

# existence check of fig file
if (path_fig.exists ()):
    # printing message
    print ("ERROR: Fig file '%s' exists." % (file_fig) )
    # exit
    sys.exit ()

# opening FITS file
with astropy.io.fits.open (file_input) as hdu:
    # reading header and image
    header = hdu[0].header
    image  = hdu[0].data
    # if no image in PrimaryHDU, then read next HDU
    if (header['NAXIS'] == 0):
        header = hdu[1].header
        image  = hdu[1].data

# making source mask
source_mask \
    = photutils.segmentation.make_source_mask (image, threshold_for_sky,
                                               npixels=npixels,
                                               sigclip_iters=maxiters,
                                               dilate_size=dilate_size)

# making masked array
image_masked = numpy.ma.array (image, mask=source_mask)

# sigma-clipping
skybg_mean, skybg_median, skybg_stddev \
    = astropy.stats.sigma_clipped_stats (image, sigma=rejection)

# mode calculation using empirical formula
skybg_mode = 3.0 * skybg_median - 2.0 * skybg_mean

# detection threshold in ADU
threshold_adu = skybg_mode + threshold * skybg_stddev

# 2D Gaussian kernel for convolution
gaussian_sigma = gaussian_fwhm * astropy.stats.gaussian_fwhm_to_sigma
kernel = astropy.convolution.Gaussian2DKernel (gaussian_sigma, \
                                               x_size=kernel_array_size, \
                                               y_size=kernel_array_size)
kernel.normalize ()

# source detection
image_segm = photutils.segmentation.detect_sources (image, threshold_adu, \
                                                    npixels=npixels, \
                                                    kernel=kernel)

# deblending
image_deblend = photutils.segmentation.deblend_sources (image, image_segm, \
                                                        npixels=npixels, \
                                                        kernel=kernel, \
                                                        nlevels=32, \
                                                        contrast=0.001)

# making a source catalogue
catalogue = photutils.segmentation.SourceCatalog (image, image_deblend)

# making a table
table_source = catalogue.to_table ()

# writing table to a file
astropy.io.ascii.write (table_source, file_catalogue, format='commented_header')

# positions of apertures
list_x = list (table_source['xcentroid'])
list_y = list (table_source['ycentroid'])

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# axes
ax.set_xlabel ('X [pixel]')
ax.set_ylabel ('Y [pixel]')

# normalisation
norm \
    = astropy.visualization.mpl_normalize.ImageNormalize \
    ( stretch=astropy.visualization.HistEqStretch (image) )

# plotting image
im = ax.imshow (image, origin='upper', cmap='viridis', norm=norm)

# plotting marks
for i in range ( len (list_x) ):
    # making a circle to indicate location of detected source
    source = matplotlib.patches.Circle (xy=(list_x[i], list_y[i]), \
                                        radius=30, \
                                        fill=False, color="red", \
                                        linewidth=1)
    # plotting location of detected source
    ax.add_patch (source)

# saving file
fig.savefig (file_fig, dpi=225)
