#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 16:55:16 (CST) daisuke>

# importing math module
import math

# pi
pi = math.pi

# angles in degree: [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180]
list_angles = range (0, 181, 15)

# processing each angle
for a_deg in list_angles:
    # conversion from deg to rad
    a_rad = a_deg / 180.0 * pi
    # calculation of sin and cos
    sin_a = math.sin (a_rad)
    cos_a = math.cos (a_rad)
    # calculation of sin^2 a + cos^2 a
    result = sin_a**2 + cos_a**2
    # printing result
    print ("sin^2 (%5.1f deg) + cos^2 (%5.1f deg) = %f + %f = %f" \
           % (a_deg, a_deg, sin_a**2, cos_a**2, result) )
