#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/03/31 14:22:41 (CST) daisuke>
#

# file name
file_output = 'text2.data'

# text data
data_text = """Two-dimensional optical CCDs (Charge-Couple Devices) and the 
infrared arrays which are their close kin are now the type of
detectors usually used to produce direct astronomical images (that is,
simple pictures of a region of sky) at optical and infrared
wavelengths. These arrays are much more sensitive and have a much
larger useful dynamic range than the panoramic detectors used hitherto
(principally the photographic plate) and it is hardly an overstatement
to say that their widespread adoption in the past two decades has
effected a revolution in astronomy.  However, the un-processed images,
as they are obtained from CCDs, are affected by a number of
instrumental effects which must be corrected before useful results can
be obtained. This cookbook is concerned with removing these
instrumental effects in order to recover an accurate picture of the
field of sky observed. This process is normally called 'CCD data
reduction' though, figuratively at least, it can just as well be
thought of as repairing a 'heap of broken images'.

from 'The 2-D CCD Data Reduction Cookbook'
"""

# opening a file handle for writing
with open (file_output, 'w') as fh:
    # writing data to a file
    fh.write (data_text)
