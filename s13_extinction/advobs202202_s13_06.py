#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2022/04/28 14:00:55 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# importing datetime module
import datetime

# importing numpy module
import numpy

# importing astropy module
import astropy.coordinates
import astropy.stats

# importing photutils module
import photutils.centroids
import photutils.aperture

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg
import matplotlib.patches

# constructing parser object
desc   = 'aperture photometry of a star at given RA and Dec'
parser = argparse.ArgumentParser (description=desc)

# centroid measurement technique
choices_centroid = ['com', '1dg', '2dg']

# PSF models (Gaussian and Moffat)
choices_psf = ['2dg', '2dm']

# colour maps
choices_cmap = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', \
                'binary', 'gray', 'bone', 'pink', \
                'spring', 'summer', 'autumn', 'winter', \
                'cool', 'hot', 'copper', 'ocean', 'terrain', \
                'gnuplot', 'cubehelix', 'jet', 'turbo']

# adding argument
parser.add_argument ('-i', '--input', default='', \
                     help='input FITS file name')
parser.add_argument ('-o', '--output', default='', \
                     help='output data file name')
parser.add_argument ('-g', '--graphic', default='', \
                     help='output graphic file name')
parser.add_argument ('-c', '--centroid', choices=choices_centroid, \
                     default='2dg', \
                     help='centroid measurement algorithm (default: 2dg)')
parser.add_argument ('-p', '--psf', choices=choices_psf, default='2dg', \
                     help='PSF model [2dg=Gaussian, 2dm=Moffat] (default: 2dg)')
parser.add_argument ('-r', '--ra', type=float, default=-999.999, \
                     help='RA in degree')
parser.add_argument ('-d', '--dec', type=float, default=-999.999, \
                     help='Dec in degree')
parser.add_argument ('-a', '--aperture', type=float, default=2.0, \
                     help='aperture radius in FWHM (default: 2.0)')
parser.add_argument ('-w', '--halfwidth', type=int, default=20, \
                     help='half-width for centroid measurement (default: 20)')
parser.add_argument ('-s1', '--skyannulus1', type=float, default=4.0, \
                     help='inner sky annulus radius in FWHM (default: 4)')
parser.add_argument ('-s2', '--skyannulus2', type=float, default=7.0, \
                     help='outer sky annulus radius in FWHM (default: 7)')
parser.add_argument ('-t', '--threshold', type=float, default=4.0, \
                     help='threshold for sigma-clipping in sigma (default: 4)')
parser.add_argument ('-n', '--maxiters', type=int, default=100, \
                     help='maximum number of iterations (default: 100)')
parser.add_argument ('-e', '--keyword-exptime', default='EXPTIME', \
                     help='FITS keyword for exposure time (default: EXPTIME)')
parser.add_argument ('-f', '--keyword-filter', default='FILTER', \
                     help='FITS keyword for filter name (default: FILTER)')
parser.add_argument ('-m', '--keyword-airmass', default='AIRMASS', \
                     help='FITS keyword for airmass (default: AIRMASS)')
parser.add_argument ('-z', '--cmap', default='bone', choices=choices_cmap, \
                     help='choice of colour map (default: bone)')
parser.add_argument ('-l', '--resolution', type=int, default=450, \
                     help='resolution in DPI (default: 450)')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_fits             = args.input
file_output           = args.output
file_graphic          = args.graphic
centroid              = args.centroid
psf_model             = args.psf
target_ra_deg         = args.ra
target_dec_deg        = args.dec
aperture_radius_fwhm  = args.aperture
halfwidth             = args.halfwidth
skyannulus_inner_fwhm = args.skyannulus1
skyannulus_outer_fwhm = args.skyannulus2
threshold             = args.threshold
maxiters              = args.maxiters
keyword_exptime       = args.keyword_exptime
keyword_filter        = args.keyword_filter
keyword_airmass       = args.keyword_airmass
cmap                  = args.cmap
resolution            = args.resolution

# check of RA and Dec
if ( (target_ra_deg < 0.0) or (target_ra_deg > 360.0) \
     or (target_dec_deg < -90.0) or (target_dec_deg > 90.0) ):
    # printing message
    print ("Something is wrong with RA or Dec!")
    print ("Check RA and Dec you specify.")
    print ("RA  = %f deg" % target_ra_deg)
    print ("Dec = %f deg" % target_dec_deg)
    # exit
    sys.exit ()

# making pathlib objects
path_fits    = pathlib.Path (file_fits)
path_output  = pathlib.Path (file_output)
path_graphic = pathlib.Path (file_graphic)

# existence checks
if not (path_fits.exists ()):
    # printing message
    print ("The file \"%s\" does not exist!")
    # exit
    sys.exit ()
if (path_output.exists ()):
    # printing message
    print ("The file \"%s\" exists!" % file_output)
    # exit
    sys.exit ()
if (path_graphic.exists ()):
    # printing message
    print ("The file \"%s\" exists!" % file_graphic)
    # exit
    sys.exit ()

# check of FITS file name
if not (path_fits.suffix == '.fits'):
    # printing message
    print ("The file \"%s\" is not a FITS file!" % file_fits)
    print ("Check the file name.")
    # exit
    sys.exit ()

# check of output file
if (file_output == ''):
    # printing message
    print ("Output file name must be given.")
    # exit
    sys.exit ()

# check of output graphic file
if not ( (path_graphic.suffix == '.eps') or (path_graphic.suffix == '.pdf') \
         or (path_graphic.suffix == '.png') or (path_graphic.suffix == '.ps') ):
    # printing message
    print ("Output graphic file must be either EPS, PDF, PNG, or PS.")
    print ("Given graphic file name = %s" % file_graphic)
    # exit
    sys.exit ()

# date/time
now = datetime.datetime.now ().isoformat ()
    
# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    # reading header information
    header = hdu_list[0].header
    # WCS information
    wcs = astropy.wcs.WCS (header)
    # reading image data
    data   = hdu_list[0].data

# extraction of information from FITS header
exptime      = header[keyword_exptime]
filter_name  = header[keyword_filter]
airmass      = header[keyword_airmass]
    
# sky coordinate
coord_sky = astropy.coordinates.SkyCoord (target_ra_deg, target_dec_deg, \
                                          unit='deg')

# conversion from sky coordinate into pixel coordinate
coord_pix = wcs.world_to_pixel (coord_sky)

# initial guess of target position
init_x = coord_pix[0]
init_y = coord_pix[1]

# region of sub-frame for centroid measurement
subframe_xmin = int (init_x - halfwidth)
subframe_xmax = int (init_x + halfwidth + 1)
subframe_ymin = int (init_y - halfwidth)
subframe_ymax = int (init_y + halfwidth + 1)

# extracting sub-frame for centroid measurement
subframe = data[subframe_ymin:subframe_ymax, subframe_xmin:subframe_xmax]

# sky subtraction
subframe_skysub = subframe - numpy.median (subframe)

# centroid measurement
if (centroid == 'com'):
#    (x_centre, y_centre) = photutils.centroids.centroid_com (subframe_skysub)
    (x_centre, y_centre) = photutils.centroids.centroid_com (subframe)
elif (centroid == '1dg'):
#    (x_centre, y_centre) = photutils.centroids.centroid_1dg (subframe_skysub)
    (x_centre, y_centre) = photutils.centroids.centroid_1dg (subframe)
elif (centroid == '2dg'):
#    (x_centre, y_centre) = photutils.centroids.centroid_2dg (subframe_skysub)
    (x_centre, y_centre) = photutils.centroids.centroid_2dg (subframe)

# PSF fitting
subframe_y, subframe_x = numpy.indices (subframe_skysub.shape)
if (psf_model == '2dg'):
    psf_init = astropy.modeling.models.Gaussian2D (x_mean=x_centre, \
                                                   y_mean=y_centre)
elif (psf_model == '2dm'):
    psf_init = astropy.modeling.models.Moffat2D (x_0=x_centre, y_0=y_centre, \
                                                 amplitude=1.0, \
                                                 alpha=1.0, gamma=1.0)
fit = astropy.modeling.fitting.LevMarLSQFitter ()
psf_fitted = fit (psf_init, subframe_x, subframe_y, subframe_skysub, \
                  maxiter=maxiters)

# fitted PSF parameters
amplitude = psf_fitted.amplitude.value
if (psf_model == '2dg'):
    x_centre_sub = psf_fitted.x_mean.value
    y_centre_sub = psf_fitted.y_mean.value
    x_centre_psf = psf_fitted.x_mean.value + subframe_xmin
    y_centre_psf = psf_fitted.y_mean.value + subframe_ymin
    x_fwhm       = psf_fitted.x_fwhm
    y_fwhm       = psf_fitted.y_fwhm
    fwhm         = (x_fwhm + y_fwhm) / 2.0
    theta        = psf_fitted.theta.value
if (psf_model == '2dm'):
    x_centre_sub = psf_fitted.x_0.value
    y_centre_sub = psf_fitted.y_0.value
    x_centre_psf = psf_fitted.x_0.value + subframe_xmin
    y_centre_psf = psf_fitted.y_0.value + subframe_ymin
    alpha        = psf_fitted.alpha.value
    gamma        = psf_fitted.gamma.value
    fwhm         = psf_fitted.fwhm

# position of centre of star in pixel coordinate
position_pix = (x_centre_psf, y_centre_psf)

# aperture radius in pixel
aperture_radius_pix  = fwhm * aperture_radius_fwhm
skyannulus_inner_pix = fwhm * skyannulus_inner_fwhm
skyannulus_outer_pix = fwhm * skyannulus_outer_fwhm

# making aperture
apphot_aperture \
    = photutils.aperture.CircularAperture (position_pix, r=aperture_radius_pix)
apphot_annulus \
    = photutils.aperture.CircularAnnulus (position_pix, \
                                          r_in=skyannulus_inner_pix, \
                                          r_out=skyannulus_outer_pix)

# sky background estimate
sigma_clip = astropy.stats.SigmaClip (sigma=threshold, maxiters=maxiters)
apphot_sky_stats \
    = photutils.aperture.ApertureStats (data, apphot_annulus, \
                                        sigma_clip=sigma_clip)
skybg_per_pix     = apphot_sky_stats.mean
skybg_err_per_pix = apphot_sky_stats.std

# aperture photometry
phot_star    = photutils.aperture.aperture_photometry (data, apphot_aperture)
raw_flux     = phot_star['aperture_sum']
npix         = apphot_aperture.area
net_flux     = raw_flux - skybg_per_pix * npix
net_flux_err = numpy.sqrt (raw_flux + npix * skybg_err_per_pix**2)

# instrumental magnitude
instmag     = -2.5 * numpy.log10 (net_flux / exptime)
instmag_err = 2.5 / numpy.log (10) * net_flux_err / net_flux

# writing results into a file
with open (file_output, 'w') as fh:
    fh.write ("#\n")
    fh.write ("# Result of Aperture Photometry\n")
    fh.write ("#\n")
    fh.write ("#  Date/Time of Analysis\n")
    fh.write ("#   Date/Time = %s\n" % now)
    fh.write ("#\n")
    fh.write ("#  Input Parameters\n")
    fh.write ("#   FITS file                    = %s\n" % file_fits)
    fh.write ("#   RA                           = %f deg\n" % target_ra_deg)
    fh.write ("#   Dec                          = %f deg\n" % target_dec_deg)
    fh.write ("#   aperture radius              = %f in FWHM\n" \
              % aperture_radius_fwhm)
    fh.write ("#   inner sky annulus            = %f in FWHM\n" \
              % skyannulus_inner_fwhm)
    fh.write ("#   outer sky annulus            = %f in FWHM\n" \
              % skyannulus_outer_fwhm)
    fh.write ("#   half-width for centroid      = %f pixel\n" % halfwidth)
    fh.write ("#   threshold for sigma-clipping = %f in sigma\n" % threshold)
    fh.write ("#   number of max iterations     = %d\n" % maxiters)
    fh.write ("#   keyword for airmass          = %s\n" % keyword_airmass)
    fh.write ("#   keyword for exposure time    = %s\n" % keyword_exptime)
    fh.write ("#   keyword for filter name      = %s\n" % keyword_filter)
    fh.write ("#\n")
    fh.write ("#  Calculated and Measured Quantities\n")
    fh.write ("#   (init_x, init_y)             = (%f, %f)\n" \
              % (init_x, init_y) )
    fh.write ("#   (centroid_x, centroid_y)     = (%f, %f)\n" \
              % (x_centre + subframe_xmin, y_centre + subframe_ymin) )
    fh.write ("#   (centre_x, centre_y)         = (%f, %f)\n" \
              % (x_centre_psf, y_centre_psf) )
    fh.write ("#   FWHM of stellar PSF          = %f pixel\n" % fwhm)
    fh.write ("#   aperture radius              = %f pix\n" \
              % aperture_radius_pix)
    fh.write ("#   inner sky annulus            = %f pix\n" \
              % skyannulus_inner_pix)
    fh.write ("#   outer sky annulus            = %f pix\n" \
              % skyannulus_outer_pix)
    fh.write ("#   sky background level         = %f ADU per pixel\n" \
              % skybg_per_pix)
    fh.write ("#   net flux                     = %f ADU\n" % net_flux)
    fh.write ("#   net flux err                 = %f ADU\n" % net_flux_err)
    fh.write ("#   instrumental mag             = %f\n" % instmag)
    fh.write ("#   instrumental mag err         = %f\n" % instmag_err)
    fh.write ("#\n")
    fh.write ("#  Results\n")
    fh.write ("#   file, exptime, filter, centre_x, centre_y,\n"
              "#   net_flux, net_flux_err, instmag, instmag_err, airmass\n")
    fh.write ("%s %f %s %f %f %f %f %f %f %f\n" \
              % (file_fits, exptime, filter_name, x_centre_psf, y_centre_psf, \
                 net_flux, net_flux_err, instmag, instmag_err, airmass) )

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111, projection=wcs)

# axes
ax.set_xlabel ('RA')
ax.set_ylabel ('Dec')
ax.set_xlim (int (x_centre_psf - skyannulus_outer_pix * 1.2),
             int (x_centre_psf + skyannulus_outer_pix * 1.2) )
ax.set_ylim (int (y_centre_psf - skyannulus_outer_pix * 1.2),
             int (y_centre_psf + skyannulus_outer_pix * 1.2) )

# plotting image
norm \
    = astropy.visualization.mpl_normalize.ImageNormalize \
    ( stretch=astropy.visualization.HistEqStretch (data) )
im = ax.imshow (data, origin='lower', cmap=cmap, norm=norm)
fig.colorbar (im)

# making a circle to indicate the location of standard star
aperture = matplotlib.patches.Circle (xy=(x_centre_psf, y_centre_psf), \
                                      radius=aperture_radius_pix, \
                                      fill=False, color="red", linewidth=2)
annulus1 = matplotlib.patches.Circle (xy=(x_centre_psf, y_centre_psf), \
                                      radius=skyannulus_inner_pix, \
                                      fill=False, color="cyan", linewidth=2)
annulus2 = matplotlib.patches.Circle (xy=(x_centre_psf, y_centre_psf), \
                                      radius=skyannulus_outer_pix, \
                                      fill=False, color="cyan", linewidth=2)
# plotting location of standard star
ax.add_patch (aperture)
ax.add_patch (annulus1)
ax.add_patch (annulus2)

# invert Y-axis
ax.invert_yaxis ()

# saving file
fig.savefig (file_graphic, dpi=resolution)
