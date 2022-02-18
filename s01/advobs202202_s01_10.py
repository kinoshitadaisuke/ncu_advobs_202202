#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 15:58:04 (CST) daisuke>

# flux of object 1
F1 = 30.0

# magnitude of object 1
m1 = 5.21

# magnitude of object 2
m2 = 9.65

# calculation of flux of object 2 using Pogson's formula
F2 = F1 * 10**(0.4 * (m1 - m2) )

# printing result
print ("m1 = %f" % m1)
print ("F1 = %f Jy" % F1)
print ("m2 = %f" % m2)
print ("F2 = F1 * 10**(0.4 * (m1 - m2) ) = %f Jy" % F2)
