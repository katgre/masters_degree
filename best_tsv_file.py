import pandas as pd
import csv

# creating two lists of H_best which will be added to the csv file later - globally
H_APEERMAG3 = []
H_APERMAG3ERR = []

def fun(x):
  
  if (np.isnan(x[2]) == False) and (np.isnan(x[4]) == False):
    # average
    H = np.round((x[2]+ x[4])/2, 4)
    # propagate error
    H_ERR = np.round(0.5 * np.sqrt((x[3]**2 + x[5]**2)), 6)
    H_APEERMAG3.append(H)
    H_APERMAG3ERR.append(H_ERR)

  # if there is only one value we leave it be
  elif (np.isnan(x[2]) == False) and (np.isnan(x[4]) == True):
    H = x[2]
    H_ERR = x[3]
    H_APEERMAG3.append(H)
    H_APERMAG3ERR.append(H_ERR)

  elif (np.isnan(x[2]) == True) and (np.isnan(x[4]) == False):
    H = x[4]
    H_ERR = x[5]
    H_APEERMAG3.append(H)
    H_APERMAG3ERR.append(H_ERR)

  return None

def best_H(name, file):

  df=pd.read_csv(f'/content/drive/Shareddrives/Magisterka_materiały/H21_500.tsv',sep='\t')

  # dropping every row that doesn't have a value in H1 nor in H2
  df = df.dropna(subset=['H_1APERMAG3', 'H_2APERMAG3'], how='all')

  # a function creating the best H - averaging if there're H1 and H2, leaving H1/H2 if there's only one value
  test = np.apply_along_axis(lambda x: fun(x), 1, df)

  # adding two columns with H_best
  df['H_APEERMAG3'] = H_APEERMAG3 
  df['H_APERMAG3ERR'] = H_APERMAG3ERR

  # deleting unnecessary columns
  df.drop(['H_1APERMAG3', 'H_1APERMAG3ERR', 'H_2APERMAG3', 'H_2APERMAG3ERR'], inplace=True, axis=1)

  # saving the finished file
  df.to_csv(f'/content/drive/Shareddrives/Magisterka_materiały/{name}_H.tsv', mode='w', sep='\t', index=False)  

  return None

# an example

best_H('OB121396', '/content/drive/Shareddrives/Magisterka_materiały/H21_500.tsv')
