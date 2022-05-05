#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/05/05 16:05:28 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing astropy module
import astropy.io.fits

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# constructing parser object
desc   = "making a histogram"
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-i', '--input', default='', help='input FITS file')
parser.add_argument ('-o', '--output', default='', help='output file')
parser.add_argument ('-a', '--z1', type=float, default=0.0, \
                     help='minimum pixel value to plot (default: 0)')
parser.add_argument ('-b', '--z2', type=float, default=70000.0, \
                     help='maximum pixel value to plot (default: 70000)')
parser.add_argument ('-n', '--nbins', type=int, default=7000, \
                     help='number of bins (default: 7000)')
parser.add_argument ('-r', '--resolution', type=int, default=450, \
                     help='resolution of output image (default: 450 DPI)')

# parsing arguments
args = parser.parse_args ()

# input parameters
file_input  = args.input
file_output = args.output
z1          = args.z1
z2          = args.z2
nbins       = args.nbins
resolution  = args.resolution

# making a pathlib object
path_input  = pathlib.Path (file_input)
path_output = pathlib.Path (file_output)

# existence checks of files
if not (path_input.exists ()):
    # printing message
    print ("ERROR: input file does not exist.")
    # exit
    sys.exit ()
if (path_output.exists ()):
    # printing message
    print ("ERROR: output file exists.")
    # exit
    sys.exit ()

# check of input FITS file
if not (path_input.suffix == '.fits'):
    # printing message
    print ("ERROR: input file must be a FITS file.")
    print ("ERROR: given input file name = %s" % file_input)
    # exit
    sys.exit ()

# check of output file
if not ( (path_output.suffix == '.eps') or (path_output.suffix == '.pdf') \
         or (path_output.suffix == '.png') or (path_output.suffix == '.ps') ):
    # printing message
    print ("ERROR: output file must be either EPS, PDF, PNG, or PS.")
    print ("ERROR: given output file name = %s" % file_output)
    # exit
    sys.exit ()

# opening FITS file
with astropy.io.fits.open (file_input) as hdu_list:
    # reading image data
    data = hdu_list[0].data

# flattening data
data_flat = data.flatten ()

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# axes
ax.set_xlabel ("Pixel Value [ADU]")
ax.set_ylabel ("Number of pixels")

# plotting image
ax.set_xlim (z1, z2)
ax.hist (data_flat, bins=nbins, range=(z1, z2), histtype='bar', align='mid', \
         label=file_input)
ax.legend ()

# saving file
fig.savefig (file_output, dpi=resolution)
