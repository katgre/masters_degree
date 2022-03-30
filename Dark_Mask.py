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

def Dark_mask(direction, camname):

  dark_file_name = f'Master_Dark_{camname}.fits'

  # Reading the Master Darks as CCD data
  Master_Dark = ccdproc.CCDData.read(f'{direction}/{dark_file_name}', unit="adu")

  # Creating a mask
  Dark_mask = ccdproc.ccdmask(Master_Dark) 

  # Saving the mask as a .fits file
  mask_as_ccd = CCDData(data=Dark_mask.astype('uint8'), unit=u.dimensionless_unscaled)
  mask_as_ccd.header['imagetyp'] = 'dark mask'

  # Deleting the existing Mask file (to avoid an error)
  if os.path.exists(f'{direction}/Dark_Mask_{camname}.fits'):
    os.remove(f'{direction}/Dark_Mask_{camname}.fits')
    mask_as_ccd.write(f'{direction}/Dark_Mask_{camname}.fits')
  else:
    mask_as_ccd.write(f'{direction}/Dark_Mask_{camname}.fits')

  return None

# Calling the sets of data we use:
Dark_mask('/content/drive/Shareddrives/Magisterka_materiały/2021jun02/raw', 'narrow')
Dark_mask('/content/drive/Shareddrives/Magisterka_materiały/2021jun02/raw', 'wide')
Dark_mask('/content/drive/Shareddrives/Magisterka_materiały/2021jun03/raw', 'narrow')
Dark_mask('/content/drive/Shareddrives/Magisterka_materiały/2021jun03/raw', 'wide')
