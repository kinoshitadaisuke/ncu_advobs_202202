#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 14:31:12 (CST) daisuke>
#

# file name
file_input = 'text.data'

# opening a file for reading
fh = open (file_input, 'r')

# reading a file line-by-line
for line in fh:
    # printing each file
    print (line.strip ())

# closing a file
fh.close ()
