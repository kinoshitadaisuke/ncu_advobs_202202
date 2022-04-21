#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/21 14:25:23 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy.coordinates

# constructing parser object
desc   = "reading standard star information from file"
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('files', nargs='+', help='files to read')

# command-line argument analysis
args = parser.parse_args ()

# list of data files
list_files = args.files

# printing header
print ("# star ID, RA, Dec, r'-band mag.")

for file_data in list_files:
    # opening the file
    with open (file_data, 'r') as fh:
        # reading the file line-by-line
        for line in fh:
            # if the line starts with '#', then skip
            if (line[0] == '#'):
                continue
            # splitting the data
            records = line.split ()
            # star ID
            star_id = int (records[0])
            # RA
            ra_deg  = float (records[1])
            # Dec
            dec_deg = float (records[2])
            # r'-band magnitude
            mag_r   = float (records[9])
            # coordinates
            coord = astropy.coordinates.SkyCoord (ra_deg, dec_deg, unit='deg')
            # conversion into hmsdms format
            radec_str = coord.to_string ('hmsdms')
            ra_str    = radec_str.split ()[0]
            dec_str   = radec_str.split ()[1]
            # printing coordinate
            print ("%03d  %-16s  %-16s  %6.3f" \
                   % (star_id, ra_str, dec_str, mag_r) )
