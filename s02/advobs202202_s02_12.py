#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 21:17:59 (CST) daisuke>
#

# importing argparse module
import argparse

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Normalising an image'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('fits', help='input FITS file name')
parser.add_argument ('-o', '--output', default='new.fits', \
                     help='output FITS file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_input  = args.fits
file_output = args.output

print ("input file  =", file_input)
print ("output file =", file_output)

# opening FITS file
hdu_list = astropy.io.fits.open (file_input)

# primary HDU
hdu0 = hdu_list[0]
    
# header of primary HDU
header0 = hdu0.header

# data of primary HDU
data0 = hdu0.data
    
# calculations of mean value
data_mean = numpy.mean (data0)

# printing mean value
print ("mean value of %s = %f" % (file_input, data_mean) )

# normalisation
data_new = data0 / data_mean

# calculation of mean value after normalisation
new_mean = numpy.mean (data_new)

# printing mean value after normalisation
print ("mean value after normalisation = %f" % new_mean)

# printing status
print ("Now, writing a file \"%s\"..." % file_output)

# writing normalised image into a file
hdu_new = astropy.io.fits.PrimaryHDU (data=data_new, header=header0)
hdu_new.writeto (file_output)
#astropy.io.fits.writeto (file_output, data_new, header=header0)

# closing FITS file
hdu_list.close ()

# printing status
print ("Finished writing a file \"%s\"!" % file_output)
