#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/28 14:52:13 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# import numpy module
import numpy

# importing scipy module
import scipy.optimize

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# constructing parser object
desc = "determining atmospheric extinction coefficient"
parser = argparse.ArgumentParser (description=desc)

# adding argument
parser.add_argument ('-o', '--output', default='', help='output image file')
parser.add_argument ('-t', '--title', default='', help='title of the plot')
parser.add_argument ('-r', '--resolution', type=int, default=450, \
                     help='resolution of output graphic file (default: 450)')
parser.add_argument ('files', nargs='+', help='input data files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_output = args.output
list_input  = args.files
resolution  = args.resolution
title       = args.title

# making pathlib object
path_output = pathlib.Path (file_output)

# checking file_output
if (file_output == ''):
    # printing message
    print ("Output file name must be given.")
    # exit
    sys.exit ()
if not ( (path_output.suffix == '.eps') or (path_output.suffix == '.pdf') \
         or (path_output.suffix == '.png') or (path_output.suffix == '.ps') ):
    # printing message
    print ("Output image file must be either EPS, PDF, PNG, or PS.")
    print ("Given output image file name = %s" % file_output)
    # exit
    sys.exit ()

# making empty numpy arrays for data
array_instmag     = numpy.array ([])
array_instmag_err = numpy.array ([])
array_airmass     = numpy.array ([])

# processing each input data file
for file_input in list_input:
    # making pathlib object
    path_input = pathlib.Path (file_input)
    # existence check
    if not (path_input.exists ()):
        # printing message
        print ("### data file '%s' does not exist, skipping..." % file_input)
        # skip
        continue

    # opening input data file
    with open (file_input, 'r') as fh:
        # reading file line-by-line
        for line in fh:
            # if the line starts with '#', then skip
            if (line[0] == '#'):
                # skip
                continue
            # splitting line
            data = line.split ()
            # instmag, instmag_err, airmass
            instmag     = float (data[7])
            instmag_err = float (data[8])
            airmass     = float (data[9])
            # adding data to numpy arrays
            array_instmag     = numpy.append (array_instmag, instmag)
            array_instmag_err = numpy.append (array_instmag_err, instmag_err)
            array_airmass     = numpy.append (array_airmass, airmass)

# least-squares method

# initial values of coefficients of fitted function
a = 1.0
b = 1.0

# function for least-squares fitting
def func (x, a, b):
    y = a * x + b
    return y

# least-squares fitting
popt, pcov = scipy.optimize.curve_fit (func, array_airmass, array_instmag, \
                                       p0=(a,b), sigma=array_instmag_err)

# fitted coefficients
print ("popt:")
print (popt)

# covariance matrix
print ("pcov:")
print (pcov)

# fitted a and b
a_fitted = popt[0]
b_fitted = popt[1]

# degree of freedom
dof = len (array_airmass) - 2
print ("dof =", dof)

# residual
residual = array_instmag - func (array_airmass, a_fitted, b_fitted)
reduced_chi2 = (residual**2).sum () / dof
print ("reduced chi^2 =", reduced_chi2)

# errors of a and b
a_err = numpy.sqrt (pcov[0][0])
b_err = numpy.sqrt (pcov[1][1])
print ("a = %f +/- %f (%f %%)" % (a_fitted, a_err, a_err / a_fitted * 100.0) )
print ("b = %f +/- %f (%f %%)" % (b_fitted, b_err, b_err / b_fitted * 100.0) )

# fitted line
fitted_x = numpy.linspace (1.0, 2.5, 10**6)
fitted_y = a_fitted * fitted_x + b_fitted

# text for extinction coefficient
text_coeff = "extinction coefficient: %5.3f +/- %5.3f mag/airmass" \
    % (a_fitted, a_err)

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# axes
ax.set_xlabel ("Airmass")
ax.set_ylabel ("Instrumental Magnitude [mag]")
ax.invert_yaxis ()

# plotting image
ax.plot (fitted_x, fitted_y, 'm--', label='least-squares fitting')
ax.errorbar (array_airmass, array_instmag, yerr=array_instmag_err, \
             fmt='go', ecolor='black', capsize=5, \
             label='photometric standard star')
ax.text (0.05, 0.05, text_coeff, transform=ax.transAxes)
ax.set_title (title)
ax.legend ()

# saving file
fig.savefig (file_output, dpi=resolution)
