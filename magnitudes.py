import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Creating file with average magniture difference
open('magnitudes_wide.txt', 'w').close()
outfile = open(f'magnitudes_wide.txt', "a")
outfile.write("Object Delta_mag Delta_error \n")

# Calculating magnitude's difference between objects from VVV catalog and found by SexTractor
def fun(x, wide, vvv):

  Deltas_mag = []
  delta_mag = (vvv['H_APEERMAG3'][x[0]]) - (wide['H_APEERMAG3'][x[1]])
  Deltas_mag.append(delta_mag)

  return Deltas_mag

# Detecting outliers in graph mag_VVV/delta_mag
def outliers(X, Y, X_bad, Y_bad, i):

  X_good, Y_good = [], []
  y_average = np.average(Y)
  sigma_y_average = np.sqrt(np.sum([(y - y_average)**2 for y in Y])/((len(Y)-1)*len(Y)))

  # sigma2_test = np.std(X)
  sigma = np.sqrt(np.sum([(y - y_average)**2 for y in Y])/len(Y))

  for n in range(len(Y)):
    if abs(Y[n] - y_average) < 3*sigma:
      X_good.append(X[n])
      Y_good.append(Y[n])
    else:
      X_bad.append(X[n])
      Y_bad.append(Y[n])

  if len(Y) == len(Y_good):
    print('Finishing {} iteration: σ = {:.5}, f(x) = {:.6} ± {:.2}, number of outliers: {}'.format(i, sigma, y_average, sigma_y_average, len(X_bad)))
    return X, Y, y_average, sigma_y_average, X_bad, Y_bad
  else:
    print('Iteration {}: σ = {:.5}, f(x) = {:.7} ± {:.2}, number of outliers: {}'.format(i, sigma, y_average, sigma_y_average, len(X_bad)))
    i += 1
    return outliers(X_good, Y_good, X_bad, Y_bad, i)

def sorting(star):

  wide = pd.read_csv(f'../{star}_narrow_H.tsv', sep = '\t')
  vvv = pd.read_csv(f'../{star}_wide_H.tsv', sep = '\t')

  df = pd.DataFrame(columns = ['vvv', 'wide', 'delta'])

  VVV, WIDE, DELTA = [], [], []
  VVV_fin, WIDE_fin, DELTA_fin = [], [], []

  for i in range(len(wide)):
    if (wide['H_APEERMAG3'][i] < (-14.2)):
      for j in range(len(vvv)):
        delta_RA = wide['RA2000'][i] - vvv['RA2000'][j]
        delta_DEC = wide['DEC2000'][i] - vvv['DEC2000'][j]
        delta = np.sqrt((delta_RA * np.cos(wide['DEC2000'][i]))**2 + (delta_DEC)**2)

        WIDE.append(i)
        VVV.append(j)
        DELTA.append(delta)

      df = pd.DataFrame(
        {'VVV': VVV,
        'WIDE': WIDE,
        'DELTA': DELTA
        })
      
      delta_fin = df[df.DELTA == df.DELTA.min()]
      VVV_fin.append(int(delta_fin['VVV']))
      WIDE_fin.append(int(delta_fin['WIDE']))
      DELTA_fin.append(float(delta_fin['DELTA'])) 

      VVV, WIDE, DELTA = [], [], []

    df2 = pd.DataFrame(
        {'VVV': VVV_fin,
        'WIDE': WIDE_fin,
        'DELTA': DELTA_fin
        })
    
  Deltas_mag = np.apply_along_axis(lambda x: fun(x, wide, vvv), 1, df2)

  X_bad, Y_bad = [], []
  i = 0

  print(f'{star}:')
  X, Y, y_average, sigma_y_average, X_bad, Y_bad = outliers([vvv['H_APEERMAG3'][m] for m in df2['VVV']], Deltas_mag, X_bad, Y_bad, i)

  outfile.write("{} {:.6} {:.6} \n".format(star, y_average, sigma_y_average))

  plt.plot(X, Y, "*", color = 'mediumpurple', label = 'fitted')
  plt.plot(X_bad, Y_bad, "*", color = 'thistle', label = "outliers")
  plt.plot(X, [y_average for x in X], label = f"f(x) = {np.round(y_average, 5)} ± {np.round(sigma_y_average, 5)} ", color = 'rebeccapurple')
  plt.gca().invert_xaxis()
  plt.xlabel('wide')
  plt.ylabel(r'$\Delta \, $mag')
  plt.title(f'{star} wide')
  plt.legend()
  plt.grid()
  plt.savefig(f'{star}_wide.png')
  plt.clf()

  return None

stars = ['OB121396', 'OB151200', 'OB121073', 'OB110284', 'OB151044', 'BLG512_18_22725']

for star in stars:
  sorting(star)

outfile.close()
  
  
  
