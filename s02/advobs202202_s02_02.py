#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 13:45:20 (CST) daisuke>
#

# importing astropy module
import astropy.units

# units
u_m  = astropy.units.m
u_pc = astropy.units.pc

# distance in pc
d_pc = 1.32 * u_pc

# converting the distance in pc into metre
d_m = d_pc.to (u_m)

# printing result
print (d_pc, "=", d_m)
