#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 15:18:51 (CST) daisuke>

# importing argparse module
import argparse

# construction of parser object
desc = 'Reading a file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-i', '--input', default='', \
                     help='input file name')

# command-line argument analysis
args = parser.parse_args()

# parameters
file_input = args.input

# initialisation of the parameter "total_price"
total_price = 0

# printing header
print ("%s" % '-' * 46)
print ("%-10s  %10s  %10s  %10s" \
       % ("fruit name", "unit price", "quantity", "sub-total") )
print ("%s" % '=' * 46)

# opening input file with read mode
with open (file_input, 'r') as fh:
    # reading the file line-by-line
    for line in fh:
        # removing line feed at the end of the line
        line = line.strip ()
        # if the line starts with "#", then skip
        if (line[0] == '#'):
            continue
        # splitting data
        (fruit_name, unit_price_str, quantity_str) = line.split ()
        # conversion from string into integer
        unit_price = int (unit_price_str)
        quantity   = int (quantity_str)
        # calculation of sub-total
        subtotal = unit_price * quantity
        # adding prices
        total_price += subtotal
        # printing sub-total
        print ("%-10s  %10d  %10d  %10d"
               % (fruit_name, unit_price, quantity, subtotal) )

# printing result
print ("%s" % '-' * 46)
print ("")
print ("Total price: %d" % total_price)
