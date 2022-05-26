# Some helper codes
'''
# Temp allow jupyter to show full df
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
  display(monthly_data_df[list(all_targeted_5_types_set)])
'''

def xaxis_label_ticker(scale_x=365, burnin_year=10):
  import matplotlib.ticker as ticker
  # Ticker function that labels x-axis in years
  #   and reflect burn-in phase of the simulation
  # Input:
  #   `scale_x` - how many days in a year, default=365
  #   `burnin_year` - how long is the burn-in phase in years, default=10
  # Return:
  #   A ticker function that labels the first day after burn-in as 0 on x-axis
  return (ticker.FuncFormatter(lambda x, pos: '{0:g}'.format((x-burnin_year*365)/scale_x)))

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

def calc_after_burin_auc_from_list(summed_genofreq_list):
  from constants import REPORTDAYS, FIRST_ROW_AFTER_BURNIN
  import numpy as np
  if len(summed_genofreq_list) == len(REPORTDAYS): # data includes burn-in
    no_burnin_summed_genofreq_list = summed_genofreq_list[FIRST_ROW_AFTER_BURNIN:]
  else:
    assert(len(summed_genofreq_list) == len(REPORTDAYS[FIRST_ROW_AFTER_BURNIN:]))
    no_burnin_summed_genofreq_list = summed_genofreq_list
  return np.trapz(
    no_burnin_summed_genofreq_list,
    x=REPORTDAYS[FIRST_ROW_AFTER_BURNIN:]
  )

def ntf_string_prep(fdir_path, range_95=False):
  from constants import SUMMARY_FILE_HEADER_NAME
  import pandas as pd
  import numpy as np
  import os
  ntfs_100runs = []
  for i in range(1,101):
    df = pd.read_csv(
      os.path.join(fdir_path, f'summary/{i}.txt'),
      index_col=False,
      names=SUMMARY_FILE_HEADER_NAME,
      sep='\t'
    )
    ntfs_100runs.append(df['ntf'].values[0])
  median = np.percentile(ntfs_100runs, 50)
  lq = np.percentile(ntfs_100runs, 25)
  uq = np.percentile(ntfs_100runs, 75)
  if range_95:
    llq = np.percentile(ntfs_100runs, 2.5)
    uuq = np.percentile(ntfs_100runs, 97.5)
    return f'NTF = {median:.2f} ({lq:.2f}-{uq:.2f}) ({llq:.2f}-{uuq:.2f})'
  return f'NTF = {median:.2f} ({lq:.2f}-{uq:.2f})'

# Archived in version 2
'''
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
'''
