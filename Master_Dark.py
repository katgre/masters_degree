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

def Master_Dark(direction, camname):

  Darks = []

  os.chdir(direction)
  for file in glob.glob("*.fits"):
    img = ccdproc.CCDData.read(file, unit="adu")
    try:
      if (img.header['OBJECT'] == 'dark') and (img.header['CAMNAME'] == camname):
        Darks.append(f'{direction}/' + file)
    # Masks do not have an OBJECT attribute and make an error
    except KeyError: 
      pass

  Master_Dark = ccdproc.combine(Darks, method='average', sigma_clip=True, unit="adu")

  Master_Dark.meta['combined'] = True

  dark_file_name = f'Master_Dark_{camname}.fits'

  # If the file already exist, it needs to be removed first 
  if os.path.exists(f'{direction}/{dark_file_name}'):
    os.remove(f'{direction}/{dark_file_name}')
    Master_Dark.write(f'{direction}/{dark_file_name}')
  else:
    Master_Dark.write(f'{direction}/{dark_file_name}')

  return None

# Calling the function for two sets of darks (narrow and wide) and dates (02.06.21 and 03.06.21)
Master_Dark('/content/drive/Shareddrives/Magisterka_materiały/2021jun02/raw', 'narrow')
Master_Dark('/content/drive/Shareddrives/Magisterka_materiały/2021jun02/raw', 'wide')
Master_Dark('/content/drive/Shareddrives/Magisterka_materiały/2021jun03/raw', 'narrow')
Master_Dark('/content/drive/Shareddrives/Magisterka_materiały/2021jun03/raw', 'wide')
