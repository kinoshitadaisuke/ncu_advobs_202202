#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 21:40:42 (CST) daisuke>
#

# importing argparse module
import argparse

# importing datetime module
import datetime

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Normalising an image and adding comments in new file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('fits', help='FITS file')
parser.add_argument ('-o', '--output', default='new.fits', \
                     help='new FITS file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_input  = args.fits
file_output = args.output

print ("input file  =", file_input)
print ("output file =", file_output)

# date/time of now
datetime_now = datetime.datetime.utcnow ()
datetime_str = "%04d-%02d-%02dT%02d:%02d:%06.3f" \
    % (datetime_now.year, datetime_now.month, datetime_now.day, \
       datetime_now.hour, datetime_now.minute, \
       datetime_now.second + datetime_now.microsecond * 10**-6)

# opening FITS file
hdu_list = astropy.io.fits.open (file_input)

# primary HDU
hdu0 = hdu_list[0]
    
# header of primary HDU
header0 = hdu0.header

# data of primary HDU
data0 = hdu0.data
    
# calculations of statistical values
data_mean = numpy.mean (data0)

# printing mean value
print ("mean value of %s = %f" % (file_input, data_mean) )

# normalisation
data_new = data0 / data_mean

# calculation of mean value after normalisation
new_mean = numpy.mean (data_new)

# printing mean value after normalisation
print ("mean value after normalisation = %f" % new_mean)

# adding new comments to header
header0['history'] = "updated on %s" % datetime_str
header0['comment'] = "image was normalised"
header0['comment'] = "mean value before normalisation was %f" % data_mean

# printing status
print ("Now, writing a file \"%s\"..." % file_output)

# writing normalised image into a file
astropy.io.fits.writeto (file_output, data_new, header=header0)

# closing FITS file
hdu_list.close ()

# printing status
print ("Finished writing a file \"%s\"!" % file_output)
