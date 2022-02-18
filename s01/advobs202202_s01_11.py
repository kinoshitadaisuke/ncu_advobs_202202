#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 16:11:25 (CST) daisuke>

# importing math module
import math

# value of pi
pi = math.pi

# diameter of the Moon in km
diameter = 3476

# mean distance from the Earth to the Moon in km
distance = 384400

# angular diameter of the Moon in radian
a_rad = diameter / distance

# conversion from radian into degree
a_deg = a_rad / pi * 180

# conversion from degree into arcmin
a_arcmin = a_deg * 60

# printing result
print ("angular diameter of the Moon = %f arcmin" % a_arcmin)
