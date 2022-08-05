import numpy as np

def range(name, ra, dec):

  # the object is around in the middle of the fits file , however I've added an additional 20 arcsec buffer 
  arcsec =  0.00555556 # 20 arcsec

  # the curvature of the Earth taken into account
  ra_min = ra + (arcsec/np.cos(dec))
  ra_max = ra - (arcsec/np.cos(dec))

  dec_min = dec - arcsec
  dec_max = dec + arcsec

  # A format required for constraining the data 
  print(f'{name}')
  if ra_max > ra_min:
    print("RA: >{} & <{}".format(np.round(ra_min, 6), np.round(ra_max, 6)))
  else:
    print("RA: >{} & <{}".format(np.round(ra_max, 6), np.round(ra_min, 6)))
  print("DEC: >{} & <{}".format(np.round(dec_min, 6), np.round(dec_max, 6)))

  return None

# an example
# OB121396 - BLG501.31.5900 
# 17:50:42.45 -29:24:49.7 (converted using https://www.astrouw.edu.pl/~jskowron/ra-dec/)

range('OB121396', 267.6768750, -29.4138056)
