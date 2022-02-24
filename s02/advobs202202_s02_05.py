#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 15:28:15 (CST) daisuke>
#

# importing argparse module
import argparse

# importing numpy module
import numpy

# importing astropy module
import astropy
import astropy.modeling.models
import astropy.units

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# construction of parser object
desc = 'plotting blackbody models'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-o', help='output file name')
parser.add_argument ('T', nargs='+', type=float, \
                     help='list of blackbody temperatures in K')

# command-line argument analysis
args = parser.parse_args ()

# parameters
file_output = args.o
list_T      = args.T

# number of blackbody models
n_bb = len (list_T)

# units
unit_micron = astropy.units.micron
unit_K      = astropy.units.K

# wavelength
wl_min = -8.0
wl_max = -4.0
n_wl   = 10**4
wl     = numpy.logspace (wl_min, wl_max, num=n_wl) * 10**6 * unit_micron

# making an empty list for blackbody data
bb_data = []

# blackbody radiation
for T in list_T:
    # temperature
    T = T * unit_K
    # making a blackbody model
    bb = astropy.modeling.models.BlackBody (temperature=T)
    # generating blackbody curve data
    bb_data.extend ([bb (wl)])

# making objects "fig" and "ax" for plotting
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# labels
label_x = 'Wavelength [micron]'
label_y = 'Spectral Radiance [erg sec^-1 cm^-2, sr^-1 Hz^-1]'
ax.set_xlabel (label_x)
ax.set_ylabel (label_y)

# axes
ax.set_xscale ('log')
ax.set_yscale ('log')
ax.set_xlim (0.01, 100)
ax.set_ylim (10**-10, 10**0)
ax.grid ()
#ax.ticklabel_format (axis='y', style='sci', scilimits=(0,0))

# plotting data
for i in range (n_bb):
    # temperature
    T_str = "%d K blackbody" % list_T[i]
    # plotting data
    ax.plot (wl, bb_data[i], '-', linewidth=3, label=T_str)
ax.legend ()

# saving the plot into a file
fig.savefig (file_output, dpi=225)
