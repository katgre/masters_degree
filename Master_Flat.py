# Before running the program make sure the ccdproc is installed (https://github.com/astropy/ccdproc)
# To install: pip install ccdproc

# For ccdproc

import numpy as np 
import scipy
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.nddata import CCDData
import ccdproc
import astropy

# For reading files
import os
import glob

# For disabling warnings (they are not useful in this case)
import warnings
warnings.filterwarnings("ignore")

def Master_Flat(direction, camname): 
  # Temporary substracted Flats that were made to make the Master Flat will be deleted

  Flats_subtract = []

  dark_file_name = f'Master_Dark_{camname}.fits'

  Master_Dark = ccdproc.CCDData.read(f'{direction}/{dark_file_name}', unit="adu")

  os.chdir(direction)
  for file in glob.glob("*.fits"):
    img = ccdproc.CCDData.read(file, unit="adu")
    try:
      if (img.header['OBJECT'] == 'flat') and (img.header['CAMNAME'] == camname):
        # Substracting the Master Dark and making a temporary .fits file with a substracted flat
        img_subtract = ccdproc.subtract_dark(img, Master_Dark, dark_exposure=astropy.units.Quantity(Master_Dark.header['ITIME']), data_exposure=astropy.units.Quantity(img.header['ITIME']), exposure_unit=u.second)
        img_subtract_name = f'{file}_subtract.fits'
        img_subtract.write(f'{direction}/{img_subtract_name}')
        Flats_subtract.append(f'{direction}/' + img_subtract_name)

    # Masks, which have been done, do not have an OBJECT attribute and make an error
    except KeyError: 
      pass
  
  Master_Flat = ccdproc.combine(Flats_subtract, method='average', sigma_clip=True, unit="adu") 

  Master_Flat.meta['combined'] = True

  flat_file_name = f'Master_Flat_{camname}.fits'

    # If the file already exist, it needs to be removed first 
  if os.path.exists(f'{direction}/{flat_file_name}'):
    os.remove(f'{direction}/{flat_file_name}')
    Master_Flat.write(f'{direction}/{flat_file_name}')
  else:
    Master_Flat.write(f'{direction}/{flat_file_name}')

  # Deleting all substracted flats
  for filename in glob.glob(f'{direction}/*subtract.fits'):
    os.remove(filename) 
 
  return None

# The sets of data we use:
Master_Flat('/content/drive/Shareddrives/Magisterka_materiały/2021jun02/raw', 'narrow')
Master_Flat('/content/drive/Shareddrives/Magisterka_materiały/2021jun02/raw', 'wide')
Master_Flat('/content/drive/Shareddrives/Magisterka_materiały/2021jun03/raw', 'narrow')
Master_Flat('/content/drive/Shareddrives/Magisterka_materiały/2021jun03/raw', 'wide')
