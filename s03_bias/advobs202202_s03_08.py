#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/03 22:36:48 (CST) daisuke>
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

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# construction of parser object
desc = 'Reading a FITS file and constructing a histogram'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-i', '--input', default='test.fits', \
                     help='intput FITS file')
parser.add_argument ('-o', '--output', default='test.png', \
                     help='output image file')
parser.add_argument ('-a', '--min', type=float, default=400.0, \
                     help='minimum value for histogram')
parser.add_argument ('-b', '--max', type=float, default=800.0, \
                     help='maximum value for histogram')
parser.add_argument ('-w', '--width', type=int, default=1.0, \
                     help='width of a bin for histogram')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
file_input  = args.input
file_output = args.output

# parameters
a     = args.min
b     = args.max
width = args.width
nbin  = int ( (b - a) / width ) + 1

# if input file is not a FITS file, then skip
if not (file_input[-5:] == '.fits'):
    # printing a message
    print ("Error: input file must be a FITS file!")
    # exit
    sys.exit ()

# if output file is not either PNG, PDF, or PS, then skip
if not ( (file_output[-4:] == '.eps') or (file_output[-4:] == '.pdf') \
         or (file_output[-4:] == '.png') or (file_output[-3:] == '.ps') ):
    # printing a message
    print ("Error: output file must be a PNG or PDF or PS!")
    # exit
    sys.exit ()

# existence check of input file using pathlib module
path_file_input = pathlib.Path (file_input)
if not (path_file_input.exists ()):
    # printing a message
    print ("Error: input file \"%s\" does not exist!" % file_input)
    # exit
    sys.exit ()

# existence check of output file using pathlib module
path_file_output = pathlib.Path (file_output)
if (path_file_output.exists ()):
    # printing a message
    print ("Error: output file \"%s\" exists!" % file_output)
    # exit
    sys.exit ()
    
# if a >= b, then skip
if (a >= b):
    # printing a message
    print ("maximum value \"a\" must be greater than minimum value \"b\".")
    # exit
    sys.exit ()
    
# opening FITS file
hdu_list = astropy.io.fits.open (file_input)

# primary HDU
hdu0 = hdu_list[0]

# reading header
header0 = hdu0.header

# reading data
data0 = hdu0.data

# closing FITS file
hdu_list.close ()

# initialisation of Numpy arrays for histogram
histogram_x = numpy.linspace (a, b, nbin)
histogram_y = numpy.zeros (nbin, dtype='int64')

# making a histogram
for i in range ( len (data0) ):
    for j in range ( len (data0[i]) ):
        # skipping data if it is outside the range [a, b]
        if ( (data0[i][j] > b) or (data0[i][j] < a) ):
            continue
        # counting
        histogram_y[int ( (data0[i][j] - a) / width)] += 1

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# labels
label_x = 'Pixel Value [ADU]'
label_y = 'Number of Pixels'
ax.set_xlabel (label_x)
ax.set_ylabel (label_y)

# plotting histogram
ax.bar (histogram_x, histogram_y, width, edgecolor='black', \
        linewidth=0.3, align='edge', label='Pixel values')
ax.legend ()

# saving the figure to a file
fig.savefig (file_output, dpi=450)
