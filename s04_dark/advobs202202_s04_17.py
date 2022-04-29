#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/11 00:51:14 (CST) daisuke>
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
import astropy.stats

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# making empty numpy arrays for plotting
data_exptime = numpy.array ([], dtype='float64')
data_mean    = numpy.array ([], dtype='float64')
data_stddev  = numpy.array ([], dtype='float64')

# construction of parser object
desc = 'Making a plot of exposure time vs mean pixel value of dark frame'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
choices_rejection = ['none', 'sigclip']
choices_cenfunc   = ['mean', 'median']
parser.add_argument ('-r', '--rejection', choices=choices_rejection, \
                     default='none', \
                     help='outlier rejection algorithm (default: none)')
parser.add_argument ('-t', '--threshold', type=float, default=4.0, \
                     help='rejection threshold in sigma')
parser.add_argument ('-n', '--maxiters', type=int, default=10, \
                     help='maximum number of iterations')
parser.add_argument ('-c', '--cenfunc', choices=choices_cenfunc, \
                     default='mean', \
                     help='method to estimate centre value (default: mean)')
parser.add_argument ('-o', '--output', default='dark.png', \
                     help='output image file')
parser.add_argument ('-d', '--resolution', type=int, default=450, \
                     help='resolution of output file (default: 450 dpi)')
parser.add_argument ('files', nargs='+', help='input FITS files')

# command-line argument analysis
args = parser.parse_args ()

# parameters given by command-line arguments
list_input  = args.files
file_output = args.output
rejection   = args.rejection
threshold   = args.threshold
cenfunc     = args.cenfunc
maxiters    = args.maxiters
resolution  = args.resolution

# checking input files
for file_fits in list_input:
    # if the file is not a FITS file, then stop the script
    if not (file_fits[-5:] == '.fits'):
        # printing error message
        print ("ERROR: Input files must be FITS files!")
        print ("ERROR: The file \"%s\" is not a FITS file!" % file_fits)
        # exit the script
        sys.exit ()
    # existence check
    path_fits = pathlib.Path (file_fits)
    if not (path_fits.exists ()):
        # printing error message
        print ("ERROR: the file \"%s\" does not exist!" % file_fits)
        # exit the script
        sys.exit ()
        
# checking output file
# if the file is not a PNG or PDF or PS file, then stop the script
if not ( (file_output[-4:] == '.eps') or (file_output[-4:] == '.pdf') \
         or (file_output[-4:] == '.png') or (file_output[-3:] == '.ps') ):
    # printing error message
    print ("Output file must be EPS, or PDF, or PNG, or PS file!")
    # exit the script
    sys.exit ()
# existence check
path_output = pathlib.Path (file_output)
if (path_output.exists ()):
    # printing error message
    print ("ERROR: the file \"%s\" exists!" % file_output)
    # exit the script
    sys.exit ()

# reading FITS files and calculating mean and stddev
for file_fits in list_input:
    # opening FITS file
    hdu_list = astropy.io.fits.open (file_fits)

    # primary HDU
    hdu0 = hdu_list[0]

    # reading header
    header0 = hdu0.header

    # reading data
    data0 = hdu0.data

    # closing FITS file
    hdu_list.close ()

    # exposure time
    exptime = header0['EXPTIME']

    # mean value
    if (rejection == 'sigclip'):
        # calculation of mean, median, and stddev using sigma-clipping
        mean, median, stddev \
            = astropy.stats.sigma_clipped_stats (data0, sigma=threshold, \
                                                 maxiters=maxiters, \
                                                 cenfunc=cenfunc, \
                                                 stdfunc='std')
    elif (rejection == 'none'):
        # calculation of simple mean and stddev
        mean   = numpy.nanmean (data0)
        stddev = numpy.nanstd (data0)

    # appending data to numpy arrays
    data_exptime = numpy.append (data_exptime, exptime)
    data_mean    = numpy.append (data_mean, mean)
    data_stddev  = numpy.append (data_stddev, stddev)

# printing data which will be used for plotting
print ("data_exptime:")
print (data_exptime)
print ("data_mean:")
print (data_mean)
print ("data_stddev:")
print (data_stddev)

# plotting using Matplotlib

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# axes
ax.set_title ('Dark Current Generation Rate')
ax.set_xlabel ('Exposure Time [sec]')
ax.set_ylabel ('Mean Pixel Value [ADU]')

# plotting a figure
ax.errorbar (data_exptime, data_mean, yerr=data_stddev, \
             fmt='bo', ecolor='black', capsize=5, label='Dark Current')
ax.legend ()

# saving the figure to a file
fig.savefig (file_output, dpi=resolution)
