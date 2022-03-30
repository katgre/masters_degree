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

def Substract(direction, camname):

  Dark_Master = ccdproc.CCDData.read(f'{direction}/Master_Dark_{camname}.fits', unit="adu")
  Flat_Master = ccdproc.CCDData.read(f'{direction}/Master_Flat_{camname}.fits', unit="adu")

  # Folder for the reduced images - in case something goes bad
  directory_reduced_raw = f'{direction}/reduced_raw'

  os.chdir(direction)
  for file in glob.glob("*.fits"):
    img = ccdproc.CCDData.read(file, unit="adu")
    try:
      if not (img.header['OBJECT'] == 'flat' or img.header['OBJECT'] == 'dark' or img.header['OBJECT'] == 'sky' or img.header['OBJECT'] == 'Seeing' or img.header['OBJECT'] == 'eng423' or img.header['OBJECT'] == 'eng428' or img.header['OBJECT'] == 'test_flat') and (img.header['CAMNAME'] == camname):
        img_substracted_dark = ccdproc.subtract_dark(img, Dark_Master, dark_exposure=astropy.units.Quantity(Dark_Master.header['ITIME']), data_exposure=astropy.units.Quantity(img.header['ITIME']), exposure_unit=u.second)
        img_substracted_dark_corr_flat = ccdproc.flat_correct(img_substracted_dark, Flat_Master)
        img_substracted_dark_corr_flat_name = f'{file}'

        # If the files already existed
        if os.path.exists(f'{directory_reduced_raw}/{img_substracted_dark_corr_flat_name}'):
          os.remove(f'{directory_reduced_raw}/{img_substracted_dark_corr_flat_name}')
          img_substracted_dark_corr_flat.write(f'{directory_reduced_raw}/{img_substracted_dark_corr_flat_name}')
        else:
          img_substracted_dark_corr_flat.write(f'{directory_reduced_raw}/{img_substracted_dark_corr_flat_name}')

    # Masks do not have an OBJECT attribute and make an error
    except KeyError: 
      pass

  return None

# Using the data:
Substract('/content/drive/Shareddrives/Magisterka_materiały/2021jun02/raw', 'narrow')
Substract('/content/drive/Shareddrives/Magisterka_materiały/2021jun02/raw', 'wide')
Substract('/content/drive/Shareddrives/Magisterka_materiały/2021jun03/raw', 'narrow')
Substract('/content/drive/Shareddrives/Magisterka_materiały/2021jun03/raw', 'wide')
