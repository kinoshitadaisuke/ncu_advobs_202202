#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 15:23:05 (CST) daisuke>

# importing argparse module
import argparse

# construction of parser object
desc = 'Finding prime numbers'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-o', '--output', default='primenumbers.data', \
                     help='output file name')
parser.add_argument ('-s', '--start', type=int, default=2, \
                     help='number to start')
parser.add_argument ('-e', '--end', type=int, default=100, \
                     help='number to end')

# command-line argument analysis
args = parser.parse_args()

# parameters
file_output = args.output
n_start     = args.start
n_end       = args.end

# initialisation of a list to store results
primenumbers = []

# checking numbers from n_start to n_end
for i in range (n_start, n_end + 1):
    # resetting the parameter "count"
    count = 0
    # examining if the number is divisible by numbers between 2 and (i-1)
    for j in range (2, i):
        # if the number is divisible, then adding 1 to "count"
        if (i % j == 0):
            count += 1
            # if count is >= 1, the number is not a prime number
            break
    # if the number is a prime number, add it to the list "primenumbers"
    if (count == 0):
        primenumbers.append (i)

# writing result into a file
with open (file_output, 'w') as fh:
    # for each prime number
    for i in primenumbers:
        # writing the number to the file
        fh.write ("%d\n" % i)
