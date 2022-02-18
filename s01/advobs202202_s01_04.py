#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 13:50:57 (CST) daisuke>

# importing argparse module
import argparse

# construction of parser object
desc = 'Arithmetic operation of two numbers'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('n1', type=float, default=1.0, help='number 1')
parser.add_argument ('operator', choices=['+', '-', 'x', '/'], \
                     default='+', help='operator (one of [+, -, x, /])')
parser.add_argument ('n2', type=float, default=1.0, help='number 2')

# command-line argument analysis
args = parser.parse_args()

# two numbers
n1       = args.n1
operator = args.operator
n2       = args.n2

# calculation
if (operator == '+'):
    n3 = n1 + n2
elif (operator == '-'):
    n3 = n1 - n2
elif (operator == 'x'):
    n3 = n1 * n2
elif (operator == '/'):
    n3 = n1 / n2

# printing result
print ("%f %s %f = %f" % (n1, operator, n2, n3) )
