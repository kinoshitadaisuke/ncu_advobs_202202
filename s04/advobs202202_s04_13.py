#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/10 23:09:26 (CST) daisuke>
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

# construction of parser object
desc = 'Reading a FITS file and making a PNG file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-a', '--min', type=float, default=0.0, \
                     help='minimum pixel value')
parser.add_argument ('-b', '--max', type=float, default=65535.0, \
                     help='maximum pixel value')
parser.add_argument ('-i', '--input', default='test.fits', \
                     help='intput FITS file')
parser.add_argument ('-o', '--output', default='test.png', \
                     help='output image file')
parser.add_argument ('-r', '--resolution', type=int, default=450, \
                     help='resolution of output file (default: 450 dpi)')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
file_input  = args.input
file_output = args.output
vmin        = args.min
vmax        = args.max
resolution  = args.resolution

# if input file is not a FITS file, then skip
if not (file_input[-5:] == '.fits'):
    # printing a message
    print ("Error: input file must be a FITS file!")
    # exit
    sys.exit ()

# if output file is not either EPS, PDF, PNG, or PS, then skip
if not ( (file_output[-4:] == '.eps') or (file_output[-4:] == '.pdf') \
         or (file_output[-4:] == '.png') or (file_output[-3:] == '.ps') ):
    # printing a message
    print ("Error: output file must be a EPS, PDF, PNG, or PS!")
    # exit
    sys.exit ()

# input file existence check
path_input = pathlib.Path (file_input)
if not (path_input.exists ()):
    # printing a message
    print ("Error: the file \"%s\" does not exists!" % file_input)
    # exit
    sys.exit ()

# output file existence check
path_output = pathlib.Path (file_output)
if (path_output.exists ()):
    # printing a message
    print ("Error: the file \"%s\" exists!" % file_output)
    # exit
    sys.exit ()

# printing input parameters
print ("#")
print ("# Input parameters:")
print ("#   input file  = %s" % file_input)
print ("#   output file = %s" % file_output)
print ("#   resolution of output image = %d dpi" % resolution)
print ("#   minimum value to plot      = %f" % vmin)
print ("#   maximum value to plot      = %f" % vmax)
print ("#")

# printing status
print ("# now, reading a FITS file...")

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

# printing status
print ("# finished reading a FITS file!")

# printing status
print ("# now, writing an image file...")

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# axes
ax.set_title (file_input)
ax.set_xlabel ('X [pixel]')
ax.set_ylabel ('Y [pixel]')

# plotting image
im = ax.imshow (data0, origin='lower', cmap='hot', vmin=vmin, vmax=vmax)
fig.colorbar (im)

# saving file
print ("# %s ==> %s" % (file_input, file_output) )
fig.savefig (file_output, dpi=resolution)

# printing status
print ("# finished writing an image file!")
