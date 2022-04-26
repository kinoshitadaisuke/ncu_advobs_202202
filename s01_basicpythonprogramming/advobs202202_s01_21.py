#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 22:16:29 (CST) daisuke>

# importing argparse module
import argparse

# construction of parser object
desc = 'divisible by 3?'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('numbers', type=int, nargs='+', help='numbers')

# command-line argument analysis
args = parser.parse_args ()

# numbers
numbers = args.numbers

# processing each number
for i in numbers:
    # remainder
    remainder = i % 3
    # use of "if" statement
    if (remainder == 0):
        print ("%d is divisible by 3, and remainder is 0." % i)
    elif (remainder == 1):
        print ("%d is not divisible by 3, and remainder is 1." % i)
    else:
        print ("%d is not divisible by 3, and remainder is 2." % i)
