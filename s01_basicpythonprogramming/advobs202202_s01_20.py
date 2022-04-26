#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 22:04:05 (CST) daisuke>

# counter
i = 0

# maximum value
i_max = 100

# total
total = 0

# using "while" statement
while (i <= i_max):
    # adding number to "total"
    total += i
    # incrementing "i"
    i += 1

# printing result
print ("0 + 1 + 2 + ... + %d = %d" % (i_max, total) )
