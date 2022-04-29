#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/04 01:16:27 (CST) daisuke>
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

# construction of parser object
desc = 'Examining time variation of mean bias level'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='bias frames')
parser.add_argument ('-s', '--sigma', type=float, default=5.0, \
                     help='factor for sigma clipping (default: 5.0)')
parser.add_argument ('-n', '--nmaxiter', type=int, default=10, \
                     help='maximum number of iterations (default: 10)')
parser.add_argument ('-o', '--output', default='bias.png', \
                     help='output file name (default: bias.png)')
parser.add_argument ('-r', '--resolution', type=int, default=450, \
                     help='resolution of output image (default: 450)')

# command-line argument analysis
args = parser.parse_args ()

# input FITS file
list_files  = args.files
nsigma      = args.sigma
nmaxiter    = args.nmaxiter
file_output = args.output
resolution  = args.resolution

# data
data_datetime = numpy.array ([], dtype='datetime64[ms]')
data_mean     = numpy.array ([], dtype='float64')
data_stddev   = numpy.array ([], dtype='float64')

# if input file is not a FITS file, then skip
for file_fits in list_files:
    if not (file_fits[-5:] == '.fits'):
        # printing a message
        print ("Error: input file must be FITS files!")
        # exit
        sys.exit ()

# if output file is not either EPS, PDF, PNG, or PS, then skip
if not ( (file_output[-4:] == '.eps') or (file_output[-4:] == '.pdf') \
         or (file_output[-4:] == '.png') or (file_output[-3:] == '.ps') ):
    # printing a message
    print ("Error: output file must be a PNG or PDF or PS!")
    # exit
    sys.exit ()

# processing files
for file_fits in list_files:
    print ("Now processing the file \"%s\"..." % file_fits)

    # file existence check using pathlib module
    path_file_fits = pathlib.Path (file_fits)
    if not (path_file_fits.exists ()):
        # printing a message
        print ("Error: input file \"%s\" does not exist!" % file_fits)
        # skipping to next
        continue
    
    # opening FITS file
    hdu_list = astropy.io.fits.open (file_fits)

    # primary HDU
    hdu0 = hdu_list[0]

    # reading header
    header0 = hdu0.header

    # reading data and conversion from uint16 into float64
    data0 = hdu0.data.astype (numpy.float64)

    # closing FITS file
    hdu_list.close ()

    # date/time
    date = header0['DATE-OBS']
    time = header0['TIME-OBS']
    datetime_str = "%sT%s" % (date, time)
    datetime64 = numpy.datetime64 (datetime_str)

    # sigma clipped mean and stddev
    data0_sigclip  = astropy.stats.sigma_clip (data0, sigma=nsigma, \
                                               maxiters=nmaxiter, masked=False)
    mean_sigclip   = numpy.mean (data0_sigclip)
    stddev_sigclip = numpy.std  (data0_sigclip)

    # appending data to the lists
    data_datetime = numpy.append (data_datetime, datetime64)
    data_mean     = numpy.append (data_mean, mean_sigclip)
    data_stddev   = numpy.append (data_stddev, stddev_sigclip)

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# labels
label_x = 'Date/Time [UT]'
label_y = 'Mean Bias Level [ADU]'
ax.set_xlabel (label_x)
ax.set_ylabel (label_y)
ax.xaxis.set_major_formatter (matplotlib.dates.DateFormatter ('%H:%M'))

# axis settings
y_min = 580.0
y_max = 610.0
ax.set_ylim (y_min, y_max)

# plotting data
ax.errorbar (data_datetime, data_mean, yerr=data_stddev, \
             marker='o', color='blue', markersize=3, linestyle='none', \
             ecolor='black', capsize=2, \
             label='Mean bias level')
ax.legend ()

# saving the figure to a file
fig.savefig (file_output, dpi=resolution)
