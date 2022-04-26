#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/02/24 14:46:36 (CST) daisuke>
#

# importing astropy module
import astropy
import astropy.coordinates
import astropy.units

# equatorial coordinate of Regulus (alpha Leo)
coo_regulus = astropy.coordinates.SkyCoord ('10h08m22.31s', '+11d58m02.0s', \
                                            frame='icrs')

# printing coordinate
print ("Regulus:")
print ("  (RA, Dec) = (%s, %s) = (%8.4f deg, %8.4f deg)" \
       % (coo_regulus.ra, coo_regulus.dec, \
          coo_regulus.ra.deg, coo_regulus.dec.deg) )

# transformation into ecliptic coordinate
ecl_regulus = coo_regulus.transform_to ('geocentricmeanecliptic')

# printing results
print ("  (lambda, beta) = (%f deg, %f deg)" \
       % (ecl_regulus.lon.deg, ecl_regulus.lat.deg) )

# units
u_hourangle = astropy.units.hourangle
u_deg       = astropy.units.deg

# equatorial coordinate of Antares (alpha Sco)
coo_antares = astropy.coordinates.SkyCoord ('16 29 24.46', '-26 25 55.2', \
                                            frame='icrs', \
                                            unit=(u_hourangle, u_deg) )

# printing coordinate
print ("Antares:")
print ("  (RA, Dec) = (%s, %s) = (%8.4f deg, %8.4f deg)" \
       % (coo_antares.ra, coo_antares.dec, \
          coo_antares.ra.deg, coo_antares.dec.deg) )

# transformation into galactic coordinate
gal_antares = coo_antares.transform_to ('galactic')

# printing results
print ("  (l, b) = (%f deg, %f deg)" % (gal_antares.l.deg, gal_antares.b.deg) )
