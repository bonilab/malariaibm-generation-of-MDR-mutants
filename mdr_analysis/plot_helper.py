import os
#import statistics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from constant import HEADLINE, ENCODINGDB, REPORTDAYS, FIRST_ROW_AFTER_BURNIN

def xaxis_label_ticker(scale_x=365, burnin_year=10):
  # Ticker function that labels x-axis in years
  #   and reflect burn-in phase of the simulation
  # Input:
  #   `scale_x` - how many days in a year, default=365
  #   `burnin_year` - how long is the burn-in phase in years, default=10
  # Return:
  #   A ticker function that labels the first day after burn-in as 0 on x-axis

  return (ticker.FuncFormatter(lambda x, pos: '{0:g}'.format((x-burnin_year*365)/scale_x)))

def IQR_compute(rawfilepattern, parsedatapattern, settherapyinfo):
  # This function takes in 100 output files from 
  #   simulation with the same setting, parsing them 
  #   by adding appropriate headers, and then compute
  #   the IQR for the genotype frequency and returns 
  #   three dataframes (LQ, Median, and UQ).

  allgenodf = []
  for i in range(131):
    # 361 rows of data are in output file
    allgenodf.append(pd.DataFrame(columns = range(361)))
  for j in range(1,101):
    file_name = rawfilepattern % j
    dummy_file = parsedatapattern % j
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
      # Write given line to the dummy file
      write_obj.write(HEADLINE + '\n')
      # Read lines from original file one by one and append them to the dummy file
      for line in read_obj:
        write_obj.write(line)
    df = pd.read_csv(dummy_file, index_col=False, sep='\t')
    df = df.fillna(0)
    df = df.iloc[:,:152]
    # For each file - append genotype freq to 128 sep dfs
    for (genotype, dfcounter) in zip(ENCODINGDB, range(128)):
      allgenodf[dfcounter] = allgenodf[dfcounter].append(df[genotype], ignore_index=True)
    # For each file - append bsp, population, and ntf to the last df
    allgenodf[128] = allgenodf[128].append(df['population'], ignore_index=True)
    allgenodf[129] = allgenodf[129].append(df['blood_slide_prevalence'], ignore_index=True)
    allgenodf[130] = allgenodf[130].append(df['monthly_ntf_raw'], ignore_index=True)
  
  LL_IQRdf = pd.DataFrame(columns = ['time_elapsed', 'population', 'blood_slide_prevalence', 'monthly_ntf_raw', 'ntf_percent'] + ENCODINGDB)
  L_IQRdf = pd.DataFrame(columns = ['time_elapsed', 'population', 'blood_slide_prevalence', 'monthly_ntf_raw', 'ntf_percent'] + ENCODINGDB)
  M_IQRdf = pd.DataFrame(columns = ['time_elapsed', 'population', 'blood_slide_prevalence', 'monthly_ntf_raw', 'ntf_percent'] + ENCODINGDB)
  U_IQRdf = pd.DataFrame(columns = ['time_elapsed', 'population', 'blood_slide_prevalence', 'monthly_ntf_raw', 'ntf_percent'] + ENCODINGDB)
  UU_IQRdf = pd.DataFrame(columns = ['time_elapsed', 'population', 'blood_slide_prevalence', 'monthly_ntf_raw', 'ntf_percent'] + ENCODINGDB)

  # Recombine population IQR results to three dfs
  population_IQR_result = allgenodf[128].astype('float').quantile([.05, .25, .5, .75, .95]).values.tolist()
  LL_IQRdf['population'] = population_IQR_result[0]
  L_IQRdf['population'] = population_IQR_result[1]
  M_IQRdf['population'] = population_IQR_result[2]
  U_IQRdf['population'] = population_IQR_result[3]
  UU_IQRdf['population'] = population_IQR_result[4]

  # Recombine bsp IQR results to three dfs
  bsp_IQR_result = allgenodf[129].astype('float').quantile([.05, .25, .5, .75, .95]).values.tolist()
  LL_IQRdf['blood_slide_prevalence'] = bsp_IQR_result[0]
  L_IQRdf['blood_slide_prevalence'] = bsp_IQR_result[1]
  M_IQRdf['blood_slide_prevalence'] = bsp_IQR_result[2]
  U_IQRdf['blood_slide_prevalence'] = bsp_IQR_result[3]
  UU_IQRdf['blood_slide_prevalence'] = bsp_IQR_result[4]

  # Recombine NTF IQR results to three dfs
  ntf_IQR_result = allgenodf[130].astype('float').quantile([.05, .25, .5, .75, .95]).values.tolist()
  LL_IQRdf['monthly_ntf_raw'] = ntf_IQR_result[0]
  L_IQRdf['monthly_ntf_raw'] = ntf_IQR_result[1]
  M_IQRdf['monthly_ntf_raw'] = ntf_IQR_result[2]
  U_IQRdf['monthly_ntf_raw'] = ntf_IQR_result[3]
  UU_IQRdf['monthly_ntf_raw'] = ntf_IQR_result[4]

  # Recombine genotype freq IQR results to three dfs
  for k in range(128):
    temp_IQR_result = allgenodf[k].astype('float').quantile([.05, .25, .5, .75, .95]).values.tolist()
    LL_IQRdf[ENCODINGDB[k]] = temp_IQR_result[0]
    L_IQRdf[ENCODINGDB[k]] = temp_IQR_result[1]
    M_IQRdf[ENCODINGDB[k]] = temp_IQR_result[2]
    U_IQRdf[ENCODINGDB[k]] = temp_IQR_result[3]
    UU_IQRdf[ENCODINGDB[k]] = temp_IQR_result[4]

  LL_IQRdf['time_elapsed'] = REPORTDAYS
  L_IQRdf['time_elapsed'] = REPORTDAYS
  M_IQRdf['time_elapsed'] = REPORTDAYS
  U_IQRdf['time_elapsed'] = REPORTDAYS
  UU_IQRdf['time_elapsed'] = REPORTDAYS

  LL_IQRdf['ntf_percent'] = L_IQRdf['monthly_ntf_raw'] / L_IQRdf['population'] * 100
  L_IQRdf['ntf_percent'] = L_IQRdf['monthly_ntf_raw'] / L_IQRdf['population'] * 100
  M_IQRdf['ntf_percent'] = M_IQRdf['monthly_ntf_raw'] / M_IQRdf['population'] * 100
  U_IQRdf['ntf_percent'] = U_IQRdf['monthly_ntf_raw'] / U_IQRdf['population'] * 100
  UU_IQRdf['ntf_percent'] = U_IQRdf['monthly_ntf_raw'] / U_IQRdf['population'] * 100

  LL_IQRdf.to_csv('IQR_data/%s_LL.csv' % settherapyinfo, index=False)
  L_IQRdf.to_csv('IQR_data/%s_L.csv' % settherapyinfo, index=False)
  M_IQRdf.to_csv('IQR_data/%s_M.csv' % settherapyinfo, index=False)
  U_IQRdf.to_csv('IQR_data/%s_U.csv' % settherapyinfo, index=False)
  UU_IQRdf.to_csv('IQR_data/%s_UU.csv' % settherapyinfo, index=False)

def NTF_IQR_compute(rawfilepattern):
  ntf_list = []
  for j in range(1,101):
    file_name = rawfilepattern % j
    df = pd.read_csv(file_name, index_col=False, header=None, sep='\t')
    ntf_list.append(float(df.iloc[0,11]))
  Ql = np.percentile(ntf_list, 5, interpolation = 'midpoint')
  Ql = round(Ql, 2)
  Q1 = np.percentile(ntf_list, 25, interpolation = 'midpoint')
  Q1 = round(Q1, 2)
  M = np.percentile(ntf_list, 50, interpolation = 'midpoint')
  M = round(M, 2)
  Q3 = np.percentile(ntf_list, 75, interpolation = 'midpoint')
  Q3 = round(Q3, 2)
  Qu = np.percentile(ntf_list, 75, interpolation = 'midpoint')
  Qu = round(Qu, 2)
  # return statistics.median(ntf_list)
  # return "%s (%s-%s, %s-%s)" % (M, Q1, Q3, Ql, Qu)
  return "%s (%s-%s)" % (M, Q1, Q3)

def resistant_strength_calc(pattern, drugname, option=1):
  # Drug Resistant Strength Calculation Function
  # 
  # Input:
  #   `pattern` takes in malaria geno-type encoding. e.g. 'KNF--C1x'; 
  #   `drugset` takes in a list of drug abbreviations (e.g. 'A', 'PPQ', etc.)
  #   that are interested for the scenario; `option` takes in a number `1` or `2`.
  # Output: 
  #   This function evaluates the Malaria encoding pattern and counts how many drugs (in the set) 
  #   is this genotype resistant to. The function also counts the number of genetic (mutation) events 
  #   happened regarding this genotype.
  # Option:
  #   For option 1, the function returns `drugnum` indicating how many drugs in the set is this pattern 
  #     resistant to, and `eventcount` indicating how many mutation events happened to this genotype; 
  #   For option 2, `drugnum` is the same while `allelecount` breaks down the mutation events to each allel, 
  #     e.g. '11000000' indicates mutations at *K76T* and *N86Y* when using Amodiaquine (AQ).

  if drugname == 'AL':
    drugset = ['A','LM']
  elif drugname == 'ASAQ':
    drugset = ['A','AQ']
  elif drugname == 'DHA-PPQ':
    drugset = ['A','PPQ']
  elif drugname == 'ASMQ':
    drugset = ['A','MQ']
  else:
    print("Drug name not found.")
    return None

  drugnum = 0
  allelecount = '00000000'
    
  if 'A' in drugset and pattern[5:6] == 'Y': # Artemisinin Resistant
    drugnum += 1
    allelecount = allelecount[0:5] + '1' + allelecount[6:]
        
  if 'PPQ' in drugset and pattern[6:7] == '2': # PPQ Resistant
    drugnum += 1
    allelecount = allelecount[0:6] + '1' + allelecount[7:]
        
  if 'LM' in drugset and pattern[0:3] != 'TYY': # LM Resistant
    drugnum += 1
    if pattern[0:1] == 'K': # K76T
      allelecount = '1' + allelecount[1:]
    if pattern[1:2] == 'N': # N86Y
      allelecount = allelecount[0:1] + '1' + allelecount[2:]
    if pattern[2:3] == 'F': # Y184F
      allelecount = allelecount[0:2] + '1' + allelecount[3:]
            
  if 'AQ' in drugset and pattern[0:3] != 'KNF': # AQ Resistant
    drugnum += 1
    if pattern[0:1] == 'T': # K76T
      allelecount = '1' + allelecount[1:]
    if pattern[1:2] == 'Y': # N86Y
      allelecount = allelecount[0:1] + '1' + allelecount[2:]
    if pattern[2:3] == 'Y': # Y184F
      allelecount = allelecount[0:2] + '1' + allelecount[3:]
            
  if 'MQ' in drugset: # MQ
    if not (pattern[1:2] == 'Y' and pattern[4:5] == '--'): # If Resistance exists
      drugnum += 1
      if pattern[1:2] == 'N': # N86Y
        allelecount = allelecount[0:1] + '1' + allelecount[2:]
      if pattern[3:5] != '--': # Double Copy N86Y & Y184F
        allelecount = allelecount[0:3] + '1-' + allelecount[5:]
            
  if option == 1:
    eventcount = allelecount.count('1')
    return ("%s-%s" % (drugnum, eventcount))
  return ("%s-%s" % (drugnum, allelecount))

def df_col_replace(original_df, drugset, option):
  # Dataframe Column Name Replace Function
  # 
  # Input: 
  #   `df` - dataframe object to be replaced;
  #   `drugset` - a set of drugs deployed for the simulation and thus we are interested in analyzing.
  # Output:
  #   `df` - parsed dataframe object where genotype encodings have been replaced by their correponding 
  #     drug-resistance-strength, in column names.
  #     The parsed dataframe also groups the columns with the same drug-resistance-strength.
  # Option:
  #   `1` replace column names with drug-mutation indication set 
  #     (e.g. 2-3 meaning 2-drug resistant, with 3-mutation event occured);
  #   `2` replace column name with its corresponding drug efficacy wrt. the current drugset.

  df = original_df.copy(deep=True)
  replacedict = {}

  # prepare dictionary based on resistance strength
  if option==1:
    for genotype in ENCODINGDB:
      replacedict[genotype] = resistant_strength_calc(genotype, drugset)
  # prepare dictionary based on drug efficacy
  elif option==2:
    efficacydf = pd.read_csv("https://github.com/lizhewen/PSU-CIDD-Malaria-Simulation/blob/v3.3_MDR_Eric/mdr_analysis/ef2020.csv")
    efficacydf = efficacydf.set_index('Shortname').iloc[:,1:]
    for genotype in ENCODINGDB:
      replacedict[genotype] = round(efficacydf.loc[genotype,drugset], 3)
  else:
    print("Option not found.")
    return None

  # Replace Column names with their corresponding MDR Strength   
  df.rename(columns=replacedict,inplace=True)

  # Sum-up the columns sharing the same name and return
  return df.groupby(by=df.columns, axis=1).sum()

def coloring_legend(mdr_case, option):
  # Helper function to give correct legend colors
  #   based on MDR intensity.

  # for drug-mutationEvent format
  if option == 1:
    legend_color = {
      "0-0": "#32cd32", # green for wild type
      "1-1": "#b0ebf7", # light blue
      "1-2": "#74a9cf", # medium blue
      "1-3": "#045a8d", # dark blue
      "2-2": "#fc9272", # light red
      "2-3": "#ef3b2c", # medium red
      "2-4": "#99000d"  # dark red
    }
    return legend_color.get(mdr_case)
  
  # for drug-efficacy format
  elif option == 2:
    percentage = int(mdr_case*100)
    if percentage >= 90:
      return "#32cd32" # [90,∞) - green
    elif percentage >= 80:
      return "#636363" # [80,90) - grey
    elif percentage >= 70:
      return "#74a9cf" # [70,80) - medium blue
    elif percentage >= 60:
      return "#fc9272" # [60,70) - light red
    else:
      return "#ef3b2c" # [0,60) - medium red
