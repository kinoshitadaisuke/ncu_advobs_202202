#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 13:42:46 (CST) daisuke>

# importing argparse module
import argparse

# construction of parser object
desc = 'Adding two floating point numbers'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-a', type=float, default=1.0, help='number 1')
parser.add_argument ('-b', type=float, default=1.0, help='number 2')

# command-line argument analysis
args = parser.parse_args()

# two numbers
a = args.a
b = args.b

# calculation to add two numbers
c = a + b

# printing result
print ("%f + %f = %f" % (a, b, c) )
