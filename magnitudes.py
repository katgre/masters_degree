import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

open('magnitudes_narrow.txt', 'w').close()
outfile = open(f'magnitudes_narrow.txt', "a")
outfile.write("Object Delta_mag Delta_error \n")

def fun_mag(x, wide, vvv):
  Deltas_mag = []
  delta_mag = (vvv['H_APEERMAG3'][x[0]]) - (wide['H_APEERMAG3'][x[1]])
  Deltas_mag.append(delta_mag)
  return Deltas_mag

def outliers_median(X, Y, X_bad, Y_bad, i):

  X_good, Y_good = [], []
  y_median = np.median(Y)

  # median absolute deviation
  k = 4.4478 # pkty dalsze niż 3*sigma
  MAD = np.median([np.abs(y - y_median) for y in Y])

  for n in range(len(Y)):
    if (abs(Y[n] - y_median) < k*MAD):
      X_good.append(X[n])
      Y_good.append(Y[n])
    else:
      X_bad.append(X[n])
      Y_bad.append(Y[n])

  if len(Y) == len(Y_good):
    print('Finishing {} iteration: MAD = {:.5}, f(x) = {:.6} ± {:.2}, number of outliers: {}'.format(i, MAD, y_median, MAD, len(Y_bad)))
    return X, Y, y_median, MAD, X_bad, Y_bad
  else:
    print('Iteration {}: σ = {:.5}, f(x) = {:.7} ± {:.2}, number of outliers: {}'.format(i, MAD, y_median, MAD, len(Y_bad)))
    i += 1
    return outliers_median(X_good, Y_good, X_bad, Y_bad, i)

  return y_median

def sorting(star):

  wide = pd.read_csv(f'../{star}_narrow_H.tsv', sep = '\t') 
  vvv = pd.read_csv(f'../{star}_wide_H.tsv', sep = '\t')

  wide = wide[wide.H_APEERMAG3<(-14.2)] 
  # obiekty z VVV nie mają jasności mniejszej niż ~ 14.2, potem tylko szum

  WIDE, VVV = [], []

  def delta(wide_row):
    delta_ra = vvv['RA2000']-row['RA2000']
    delta_dec = vvv['DEC2000']-row['DEC2000']
    return np.sqrt((delta_ra*np.cos(vvv['DEC2000']))**2+
                   (delta_dec)**2)

  for i, row in wide.iterrows():
    # i - indeks wide
    # indeks vvv'a ktory ma ra i dec najblizej narrowa[i]
    j = np.argmin(delta(row))
    WIDE.append(i)
    VVV.append(j)

  df = pd.DataFrame(
    {'VVV': VVV,
    'WIDE': WIDE,
    })
  
  Deltas_mag = np.apply_along_axis(lambda x: fun_mag(x, wide, vvv), 1, df)

  X_bad, Y_bad = [], []
  i = 0

  print(f'{star}:')
  X, Y, y_median, MAD, X_bad, Y_bad = outliers_median([vvv['H_APEERMAG3'][m] for m in df['VVV']], Deltas_mag.flatten(), X_bad, Y_bad, i)

  outfile.write("{:.6} {:.6} {:.6} \n".format(star, y_median, MAD))

  plt.plot(X, Y, "*", color = 'dimgray', label = 'fitted')
  plt.plot(X_bad, Y_bad, "*", color = 'lightgray', label = "outliers")
  plt.plot([vvv['H_APEERMAG3'][m] for m in df['VVV']], [y_median for x in df['VVV']], label = f"median: {np.round(y_median, 5)} ± {np.round(MAD, 5)} mag", color = 'royalblue')
  plt.legend()
  plt.grid()
  plt.xlabel('VVV')
  plt.ylabel(r'$\Delta \, $mag')
  plt.title(f'{star}')
  plt.gca().invert_xaxis()
  plt.savefig(f'{star}_wide.png')
  plt.clf()

  return None

stars = ['OB121396', 'OB151200', 'OB121073', 'OB110284', 'OB151044', 'BLG512_18_22725']

for star in stars:
  sorting(star)
