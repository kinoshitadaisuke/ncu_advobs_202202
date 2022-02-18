#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 16:21:40 (CST) daisuke>

# importing math module
import math

# luminosity of Betelgeuse
L_betelgeuse = 126000

# effective temperature of Betelgeuse
T_betelgeuse = 3600

# luminosity of the Sun
L_sun        = 1

# effective temperature of the Sun
T_sun        = 5800

# calculation of radius of Betelgeuse in solar radius
R_betelgeuse = math.sqrt (L_betelgeuse / L_sun) * (T_betelgeuse / T_sun)**-2

# printing result
print ("radius of Betelgeuse = %f solar radii" % R_betelgeuse)
