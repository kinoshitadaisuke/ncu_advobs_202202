#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 15:54:16 (CST) daisuke>

# Planck constant
h = 6.63 * 10**-34

# speed of light in vacuum
c = 3.00 * 10**8

# 1 eV in J
eV = 1.60 * 10**-19

# energy of a photon in eV
E_eV = 24.59

# calculation of energy of a photon in J
E_J = E_eV * eV

# calculation of wavelength of a photon
wavelength = h * c / E_J

# printing result
print ("energy of a photon = %f eV = %g J" % (E_eV, E_J) )
print ("wavelength = %g m = %f nm" % (wavelength, wavelength * 10**9) )
