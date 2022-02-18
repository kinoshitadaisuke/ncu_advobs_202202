#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 13:33:30 (CST) daisuke>

# importing argparse module
import argparse

# construction of parser object
parser = argparse.ArgumentParser (description='Adding two numbers')

# adding arguments
parser.add_argument ('-a', type=int, default=1, help='number 1')
parser.add_argument ('-b', type=int, default=1, help='number 2')

# command-line argument analysis
args = parser.parse_args()

# two numbers
a = args.a
b = args.b

# calculation to add two numbers
c = a + b

# printing result
print (a, '+', b, '=', c)
