#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 14:04:52 (CST) daisuke>

# importing argparse module
import argparse

# construction of parser object
desc = 'Calculation of a mean'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('numbers', type=float, nargs='+', help='a set of numbers')

# command-line argument analysis
args = parser.parse_args()

# numbers
numbers = args.numbers

# number of data
n = len (numbers)

# initialisation of a variable 'total'
total = 0.0

# adding numbers using "for"
for number in numbers:
    total += number

# calculation of a mean
mean = total / n

# printing result
print ("input data set =", numbers)
print ("number of data = %d" % n)
print ("mean value     = %f / %d = %f" % (total, n, mean) )
