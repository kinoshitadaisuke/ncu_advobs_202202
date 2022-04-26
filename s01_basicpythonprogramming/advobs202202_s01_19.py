#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 21:57:37 (CST) daisuke>

# importing math module
import math

# pi
pi = math.pi

# making a list
list_a = list (range (0, 181, 30))

# using "for" statement
for i in list_a:
    print ("sin (%03d deg) = %f" % (i, math.sin (i / 180.0 * pi) ) )

# initialising a parameter "total"
total = 0
    
# adding numbers from 0 to 10
for i in range (0, 11):
    total += i

# printing "total"
print ("0 + 1 + 2 + ... + 8 + 9 + 10 =", total)
