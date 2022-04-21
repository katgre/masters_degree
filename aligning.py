# Before running the program make sure the ccdproc is installed (https://github.com/astropy/ccdproc)
# To install: pip install ccdproc

# The older version of scikit package needs to be installed in order for astroalign to work:
# pip install scikit-image==0.15.0
# pip install astroalign

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

def align(image, image0):

  image_ccd = ccdproc.CCDData.read(image, unit='adu')
  image0_ccd = ccdproc.CCDData.read(image0, unit='adu')

  image_registered, footprint2 = astroalign.register(image_ccd, image0_ccd, propagate_mask=True)

  return image_registered

def align_combine(direction, object_name, camname):

  Images = []

  outfile = open(f'{direction}/errors.txt', "a")

  os.chdir(direction)

  for file in glob.glob("*.fits"):
    img = ccdproc.CCDData.read(file, unit="adu")
    try:
      if img.header['OBJECT'] == object_name and img.header['CAMNAME'] == camname:
        Images.append(f'{direction}/{file}') # Creating a list of objects for aligning and combining

    except KeyError: 
      pass

  try:
    combined = ccdproc.combine([ccdproc.CCDData(align(image, Images[0]), unit="adu") for image in Images[1:]], method='average')

    combined.meta['combined'] = True
    combined_file_name = f'{object_name}_{camname}.fits'

    if os.path.exists(f'{direction}/{combined_file_name}'):
      os.remove(f'{direction}/{combined_file_name}')
      combined.write(f'{direction}/{combined_file_name}')
    else:
      combined.write(f'{direction}/{combined_file_name}')

  except Exception as e:
    outfile.write("{} {} {} \n".format(object_name, camname, e))

  outfile.close()
  return None

object_name_2021jun02 = ['OB121396', 'OB151200', 'OB151044', 'OB161043']
object_name_2021jun03 = ['OB151044', 'OB121073', 'OB110284', 'BLG512_18_22725', 'OB161043', 'EROS-GSA15', 'Gaia21bfr']
camnames = ['narrow', 'wide']

for object_name in object_name_2021jun02:
  for camname in camnames:
    align_combine('/content/drive/Shareddrives/Magisterka_materiały/2021jun02/raw/reduced_raw', object_name, camname)

for object_name in object_name_2021jun03:
  for camname in camnames:
    align_combine('/content/drive/Shareddrives/Magisterka_materiały/2021jun03/raw/reduced_raw', object_name, camname)
