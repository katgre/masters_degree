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
import itertools

# For reading files
import os
import glob

# For disabling warnings (they are not useful in this case)
import warnings
warnings.filterwarnings("ignore")

# For cosmicray_lacosmic function to work properly (https://github.com/astropy/ccdproc/issues/786)
from packaging import version
version.parse('1.1.0')

def darkpoints_mask(new_image):

  # Creating a numpy array, so it can be worked on 
  img_numpy = np.array(new_image)

  # Creating a table which will be used as a mask for points with the value < 0
  mask = np.full((img_numpy.shape[0], img_numpy.shape[1]), False)

  for i in range(img_numpy.shape[0]):
    for j in range(img_numpy.shape[1]):
      if img_numpy[i, j] < 0:
        mask[i][j] = True
        try:
          mask[i+1][j] = True
          mask[i-1][j] = True
          mask[i][j+1] = True
          mask[i][j-1] = True
        except Exception as e: # for pixels outside of 1024 array
          pass  

  return mask


# For aligning images (and their masks) properly
def align(image, image0):

  image_ccd = ccdproc.CCDData.read(image, unit='adu')
  image0_ccd = ccdproc.CCDData.read(image0, unit='adu')

  # Aligning two images, image0 is a base
  image_registered, footprint = astroalign.register(image_ccd, image0_ccd, propagate_mask=True)

  # Creating a new image with a shifted mask
  new_image = ccdproc.CCDData(image_registered, unit='adu', mask=footprint) 

  mask = darkpoints_mask(new_image)

  # Adding two masks (the first one based on the dark current, the second - with negative pixels)
  new_mask = footprint | mask

  # Adding a new mask to the image
  new_image_new_mask = ccdproc.CCDData(new_image, unit='electron', mask=new_mask) 

  # Substracting cosmic rays or pixels being a result of aligning two pictures
  new_image_new_mask_cosmicrays = ccdproc.cosmicray_lacosmic(new_image_new_mask, cleantype='medmask', niter=6, sigclip = 3.5)

  return new_image_new_mask_cosmicrays


def align_combine(direction, object_name, camname):

  Images = []

  outfile = open(f'{direction}/errors.txt', "a")

  for file in itertools.chain(os.scandir(f'{direction}/2021jun02/raw/reduced_raw'), os.scandir(f'{direction}/2021jun03/raw/reduced_raw')):
    img = ccdproc.CCDData.read(file.path, unit="adu")
    try:
      if img.header['OBJECT'] == object_name and img.header['CAMNAME'] == camname:
        Images.append(file.path) # Creating a list of objects for aligning and combining

    except KeyError: 
      pass
      
  try:
    # Combining all images
    combined = ccdproc.combine([ccdproc.CCDData(align(image, Images[0]), unit="adu") for image in Images], method='average')

    # Saving a combined image
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

# List of objects for aligning
object_name_2021jun0203 = ['OB121396', 'OB151200', 'OB151044', 'OB161043', 'OB121073', 'OB110284', 'BLG512_18_22725', 'EROS-GSA15', 'Gaia21bfr']
camnames = ['narrow', 'wide']

for object_name in object_name_2021jun0203:
  for camname in camnames:
    align_combine('/content/drive/Shareddrives/Magisterka_materiały/', object_name, camname)

for object_name in object_name_2021jun03:
  for camname in camnames:
    align_combine('/content/drive/Shareddrives/Magisterka_materiały/2021jun03/raw/reduced_raw', object_name, camname)
