#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/05/19 16:50:54 (CST) daisuke>
#

# importing numpy module
import numpy
import numpy.random

# importing astropy module
import astropy.table

# generating a new astropy table
table_stars = astropy.table.Table ()

# number of stars to generate
nstars = 100

# flux of faintest stars
flux_min = 1000.0

# image size
image_size_x = 2048
image_size_y = 2048

# FWHM of PSF
fwhm_x        = 3.5
fwhm_y        = 3.5
fwhm_stddev_x = 0.1
fwhm_stddev_y = 0.1

# generating random numbers
rng        = numpy.random.default_rng ()
position_x = rng.uniform (0, image_size_x, nstars)
position_y = rng.uniform (0, image_size_y, nstars)
theta_deg  = rng.uniform (0, 360, nstars)
psf_x      = rng.normal (loc=fwhm_x, scale=fwhm_stddev_x, size=nstars)
psf_y      = rng.normal (loc=fwhm_y, scale=fwhm_stddev_y, size=nstars)
powerlaw   = rng.power (1.5, size=nstars)
flux       = flux_min / powerlaw

# conversion from degree to radian
theta_rad = numpy.radians (theta_deg)

# adding data to the table
table_stars['amplitude'] = flux
table_stars['x_mean']    = position_x
table_stars['y_mean']    = position_y
table_stars['x_stddev']  = psf_x
table_stars['y_stddev']  = psf_y
table_stars['theta']     = theta_rad

# printing table
print ("#")
print ("# Astropy table")
print ("#")
print (table_stars)

# printing table information
print ("#")
print ("# Astropy table information")
print ("#")
print (table_stars.info)
