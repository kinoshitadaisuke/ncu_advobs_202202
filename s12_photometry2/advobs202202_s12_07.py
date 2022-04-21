#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/21 20:48:17 (CST) daisuke>
#

# importing math module
import math

# importing uncertainties module
import uncertainties
import uncertainties.umath

# r'-band magnitude of star ID 12
mag_star1 = 14.339

# net flux of star ID 12
# 1712.5 +/- 41.4
flux_star1 = uncertainties.ufloat (1712.5, 41.4)

# net flux of star ID 16
# 1105.8 +/- 33.3
flux_star2 = uncertainties.ufloat (1105.8, 33.3)

# r'-band magnitude of star ID 16
mag_star2 \
    = mag_star1 - 2.5 * uncertainties.umath.log10 (flux_star2 / flux_star1)

# printing result
print ("#")
print ("# input parameters")
print ("#")
print ("#  mag_star1  =", mag_star1)
print ("#  flux_star1 =", flux_star1)
print ("#  flux_star2 =", flux_star2)
print ("#")
print ("mag_star2 =", mag_star2)
