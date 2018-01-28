import sys
import math

from pymonetdb.sql.connections import Connection as connect
from pymonetdb.exceptions import Error as DBError

#import lofar.gsm.gsmutils as gsm
from gsm import utils as gu
from gsm.config import config as cfg

# Interpret the arguments and do the selection.
def main (name, argv):

    if len(argv) < 5  or  (argv[0] == '-p'  and  len(argv) < 7):
        print ''
        print 'Insufficient arguments given; run as:'
        print ''
        print '   %s [-p patchname] basecat outfile RA DEC radius [vlssFluxCutoff [assocTheta]]' % name
        print 'to select using a cone'
        print ''
        print 'Note that for the new version you have to specify the base catalog as argument.'
        print ''
        print '   -p patchname    if given, all sources belong to this single patch'
        print '   basecat         base catalog, either TGSS or VLSS'
        print '   outfile         path-name of the output file'
        print '                   It will be overwritten if already existing'
        print '   RA              cone center Right Ascension (J2000, degrees)'
        print '   DEC             cone center Declination     (J2000, degrees)'
        print '   radius          cone radius                 (degrees)'
        print '   fluxCutoff      minimum flux (Jy) of basecat sources to use'
        print '                   (TGSS default = 0.3, VLSS default = 4)'
        print '   assocTheta      uncertainty in matching     (degrees)'
        print '                   default = 0.00278  (10 arcsec)'
        print ''
        return False

    # Get the arguments.
    patch   = ''
    st = 0
    if argv[0] == '-p':
        patch = argv[1]
        st = 2
    basecat = argv[st]
    if basecat not in ['TGSS', 'VLSS']:
        raise ValueError("'%s' is not a valid base catalog. Chose TGSS or VLSS" % (basecat))
    outfile = argv[st+1]
    try:
      ra      = float(argv[st+2])
      dec     = float(argv[st+3])
    except ValueError:
      # Try to parse ra-dec as in the output of msoverview, e.g. 08:13:36.0000 +48.13.03.0000
      ralst = argv[st+2].split(':')
      ra = math.copysign(abs(float(ralst[0]))+float(ralst[1])/60.+float(ralst[2])/3600.,float(ralst[0]))
      declst = argv[st+3].split('.')
      dec = math.copysign(abs(float(declst[0]))+float(declst[1])/60.+float('.'.join(declst[2:]))/3600.,float(declst[0]))
    radius  = float(argv[st+4])
    if basecat == 'VLSS':
        cutoff  = 4.
    else:
        cutoff  = 0.3
    theta   = 0.00278
    if len(argv) > st+5:
        cutoff = float(argv[st+5])
    if len(argv) > st+6:
        theta = float(argv[st+6])

    try:
        conn = connect(hostname = cfg.host()
                      ,database = cfg.dbname()
                      ,username = cfg.uname()
                      ,password = cfg.pword()
                      ,port = cfg.port()
                      )
        gu.expected_fluxes_in_fov(conn, basecat, ra, dec, radius,
                                  theta, outfile, flux_cutoff=cutoff, patchname=patch,
                                  storespectraplots=False, deruiter_radius=3.717)
    except DBError, e:
        raise

if __name__ == "__main__":
    try:
        main(sys.argv[0], sys.argv[1:])
    except Exception as e:
        print "Failed for reason: %s" % (e,)
