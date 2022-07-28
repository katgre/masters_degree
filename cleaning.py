# Before running the program make sure the ccdproc is installed (https://github.com/astropy/ccdproc)
# To install: pip install ccdproc

# For ccdproc
import numpy as np 
import pandas as pd
import scipy
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.nddata import CCDData
import ccdproc

# For interpolation: https://docs.astropy.org/en/stable/convolution/index.html
from astropy.convolution import Gaussian2DKernel
from astropy.convolution import interpolate_replace_nans

def cleaning(obj_filename, cam):

  # Loading an image and converting it to the numpy array, so interpolation can work
  obj = ccdproc.CCDData.read(f'/content/drive/Shareddrives/Magisterka_materiały/{obj_filename}_{cam}.fits', unit="adu")
  obj_numpy = np.array(obj)

  # Creating a kernel - ensure that it is large enough to completely cover potential contiguous regions of NaN values 
  kernel = Gaussian2DKernel(x_stddev=1, y_stddev=1)

  # Cleaning an image from NaN values and saving it as a fits file
  fixed_obj = interpolate_replace_nans(obj_numpy, kernel)
  fixed_fits = ccdproc.CCDData(fixed_obj, unit="adu")

  interpolated_file_name = f'{obj_filename}_{cam}.fits'

  fixed_fits.write(f'/content/drive/Shareddrives/Magisterka_materiały/{interpolated_file_name}', overwrite=True)

  return None

# List of objects for cleaning
object_name_2021jun0203 = ['OB121396', 'OB151200', 'OB151044', 'OB161043', 'OB121073', 'OB110284', 'BLG512_18_22725', 'EROS-GSA15', 'Gaia21bfr']

for object_name in object_name_2021jun0203:
  cleaning(object_name, 'wide')
  cleaning(object_name, 'narrow')
