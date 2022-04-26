#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 14:15:35 (CST) daisuke>

# importing argparse module
import argparse

# construction of parser object
desc = 'Calculation of average'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-a', choices=['mean', 'median'], \
                     default='mean', help='algorithm (mean or median)')
parser.add_argument ('numbers', type=float, nargs='+', help='a set of numbers')

# command-line argument analysis
args = parser.parse_args()

# numbers
algorithm = args.a
numbers   = args.numbers

# number of data
n = len (numbers)

#
# calculation of average
#

# mean calculation
if (algorithm == 'mean'):
    # initialisation of a variable 'total'
    total = 0.0
    # adding numbers
    for number in numbers:
        total += number
    # calculation of a mean
    mean = total / n
# median calculation
elif (algorithm == 'median'):
    # sorting data
    sorted_numbers = sorted (numbers)
    # calculation of a median
    if (n % 2 == 0):
        # if number of data is even number,
        # adding two numbers in the middle, then divide by two
        median = ( sorted_numbers[int (n / 2) - 1] \
                   + sorted_numbers[int (n / 2)] ) / 2.0
    elif (n % 2 == 1):
        # if number of data is odd number,
        # simply taking the number in the middle
        median = sorted_numbers[int (n / 2)]

# printing result
print ("input data     =", numbers)
print ("number of data = %d" % n)
if (algorithm == 'mean'):
    print ("mean           = %f / %d = %f" % (total, n, mean) )
elif (algorithm == 'median'):
    print ("median         = %f" % median)
