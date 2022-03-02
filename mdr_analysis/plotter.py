import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from plot_helper import xaxis_label_ticker, coloring_legend, df_col_replace
from constant import FIRST_ROW_AFTER_BURNIN, ANNOTATION_X_LOCATION

def fig1_plot_IQR(ax, dflist_arg, drug, IQR_only=False, annoty=None, marker_2_2s=False):
  option = 1
  from constant import REPORTDAYS
  REPORTDAYS = REPORTDAYS[FIRST_ROW_AFTER_BURNIN:]
  dflist = copy.deepcopy(dflist_arg) 
  # rename all 100 df's by `drug` and sum-up columns
  for i in range(len(dflist)):
    dflist[i] = df_col_replace(dflist[i], drug, option)
    dflist[i] = dflist[i].iloc[FIRST_ROW_AFTER_BURNIN:]
    dflist[i].reset_index(drop=True, inplace=True)
  # combine columns wanted into one df, for each MDR
  mdr_cases = list(dflist[0].columns)
  # print(mdr_cases)
  idx_most_dang_double = mdr_cases.index('2-2') if drug == 'DHA-PPQ' else mdr_cases.index('2-4')
  idx_2_2 = mdr_cases.index('2-2')
  # print(idx_most_dang_double)
  # print(idx_2_2)
  all_MDR_across_run = []
  for i in range(len(mdr_cases)):
    all_MDR_across_run.append(pd.DataFrame(columns=range(241))) # 241 rows of data are in output file without burn-in
  for onerun in dflist:
    for i in range(len(mdr_cases)):
      all_MDR_across_run[i] = all_MDR_across_run[i].append(onerun[mdr_cases[i]], ignore_index=True)
  # calculate 90% CI and IQR
  all_MDR_IQR = []
  for i in range(len(mdr_cases)):
    all_MDR_IQR.append(all_MDR_across_run[i].astype('float').quantile([.05, .25, .5, .75, .95]).values.tolist())
  # plot
  for i in range(len(mdr_cases)):
    mdr_case = mdr_cases[i]
    color = coloring_legend(mdr_case, option)
    ax.plot(REPORTDAYS, all_MDR_IQR[i][2], label=mdr_case, 
                    color=color)
    ax.fill_between(REPORTDAYS, all_MDR_IQR[i][1], all_MDR_IQR[i][3], 
                    color=color, alpha=0.25)
    if IQR_only == False:
      ax.fill_between(REPORTDAYS, all_MDR_IQR[i][0], all_MDR_IQR[i][4], 
                      color=color, alpha=0.1)
  # Mark where it exceeds the 1% and 10% for most-dangerous type
  idx_one_percent = -1
  idx_ten_percent = -1
  for idx,val in enumerate(all_MDR_IQR[idx_most_dang_double][2]):
    if val > 0.01:
      idx_one_percent = idx
      break
  for idx,val in enumerate(all_MDR_IQR[idx_most_dang_double][2]):
    if val > 0.1:
      idx_ten_percent = idx
      break
  if idx_one_percent != -1:
    ax.plot(REPORTDAYS[idx_one_percent], all_MDR_IQR[-1][2][idx_one_percent], 'o', color='k')
  if idx_ten_percent != -1:
    ax.plot(REPORTDAYS[idx_ten_percent], all_MDR_IQR[-1][2][idx_ten_percent], 'o', color='k')

  if marker_2_2s:
    idx_one_percent_2_2 = -1
    idx_ten_percent_2_2 = -1
    for idx,val in enumerate(all_MDR_IQR[idx_2_2][2]):
      if val > 0.01:
        idx_one_percent_2_2 = idx
        break
    for idx,val in enumerate(all_MDR_IQR[idx_2_2][2]):
      if val > 0.1:
        idx_ten_percent_2_2 = idx
        break
    if idx_one_percent_2_2 != -1:
      # print(REPORTDAYS[idx_one_percent_2_2], all_MDR_IQR[idx_2_2][2][idx_one_percent_2_2])
      ax.plot(REPORTDAYS[idx_one_percent_2_2], all_MDR_IQR[idx_2_2][2][idx_one_percent_2_2], '^', color='k')
    if idx_ten_percent_2_2 != -1:
      ax.plot(REPORTDAYS[idx_ten_percent_2_2], all_MDR_IQR[idx_2_2][2][idx_ten_percent_2_2], '^', color='k')

def fig1_plot_vars(ax, dflist, drug):
  from constant import REPORTDAYS
  REPORTDAYS = REPORTDAYS[FIRST_ROW_AFTER_BURNIN:]
  # Highest is 2-2 for DHA-PPQ
  if drug == 'DHA-PPQ':
    for df in dflist:
      df = df_col_replace(df, drug, option=1)
      df = df.iloc[FIRST_ROW_AFTER_BURNIN:]
      ax.plot(REPORTDAYS, df['2-2'], color='#fc9272', alpha=0.1)
  # Highest is 2-4 for ASAQ & AL
  else:
    for df in dflist:
      df = df_col_replace(df, drug, option=1)
      df = df.iloc[FIRST_ROW_AFTER_BURNIN:]
      ax.plot(REPORTDAYS, df['2-4'], color='#99000d', alpha=0.1)

# pattern is in regex
# dflist contains 100 dfs from output files
def fig2_dangerous_triple(ax, dflist, pattern, IQR_only=False, annoty=None, ntf=None):
  from constant import REPORTDAYS
  # combine columns wanted into one df
  df_IQR = pd.DataFrame(columns = range(361)) # 361 rows of data are in output file
  for onerun in dflist:
    df_IQR = df_IQR.append(onerun.filter(regex=pattern, axis=1).sum(axis=1), ignore_index=True)
  # calculate 90% CI and IQR
  IQR_result = df_IQR.astype('float').quantile([.05, .25, .5, .75, .95]).values.tolist()
  # remove burn-in stage from plots
  REPORTDAYS = REPORTDAYS[FIRST_ROW_AFTER_BURNIN:]
  for i in range(5):
    IQR_result[i] = IQR_result[i][FIRST_ROW_AFTER_BURNIN:]
  # plots
  ax.plot(REPORTDAYS, IQR_result[2], color='#800080') # median
  ax.fill_between(REPORTDAYS, IQR_result[1], IQR_result[3], color='#800080', alpha=0.25)
  if IQR_only == False:
    ax.fill_between(REPORTDAYS, IQR_result[0], IQR_result[4], color='#800080', alpha=0.1)
  # Mark where it exceeds the 1% and 10%
  idx_one_percent = -1
  idx_ten_percent = -1
  for idx,val in enumerate(IQR_result[2]):
    if val > 0.01:
      idx_one_percent = idx
      break
  for idx,val in enumerate(IQR_result[2]):
    if val > 0.1:
      idx_ten_percent = idx
      break
  if idx_one_percent != -1:
    ax.plot(REPORTDAYS[idx_one_percent], IQR_result[2][idx_one_percent], 'o', color='k')
    t_01 = round(REPORTDAYS[idx_one_percent]/365-10, 1)
  else:
    t_01 = 'N/A'
  if idx_ten_percent != -1:
    ax.plot(REPORTDAYS[idx_ten_percent], IQR_result[2][idx_ten_percent], 'o', color='k')
  # Calc NTF and annotate if needed
  if annoty is not None:
    # calculate genotype freq at last day
    x_20 = IQR_result[2][-1]
    x_20 = round(x_20, 3)
    # calculate area under median curve, with IQR
    auc = np.trapz(IQR_result[2], x=REPORTDAYS)
    auc = round(auc, 2)
    # lower quartile
    auc_l = np.trapz(IQR_result[1], x=REPORTDAYS)
    auc_l = round(auc_l, 2)
    # upper quartile
    auc_u = np.trapz(IQR_result[3], x=REPORTDAYS)
    auc_u = round(auc_u, 2)
    # annotate
    annotation_string = r"$x_{20}$ = %s" % x_20
    annotation_string += "\n"
    annotation_string += r"$T_{.01}$ = %s" % t_01
    annotation_string += "\n"
    annotation_string += "AUC = %s (%s-%s)" % (auc, auc_l, auc_u)
    if ntf is not None:
      annotation_string += "\n"
      annotation_string += "NTF = %s" % ntf
    ax.text(ANNOTATION_X_LOCATION, annoty*0.78, annotation_string, verticalalignment='top', size=14)

def fig2_dangerous_double(ax, dflist_arg, drug, IQR_only=False, annoty=None):
  option = 1
  from constant import REPORTDAYS
  REPORTDAYS = REPORTDAYS[FIRST_ROW_AFTER_BURNIN:]
  dflist = copy.deepcopy(dflist_arg) 
  # rename all 100 df's by `drug` and sum-up columns
  for i in range(len(dflist)):
    dflist[i] = df_col_replace(dflist[i], drug, option)
    dflist[i] = dflist[i].iloc[FIRST_ROW_AFTER_BURNIN:]
    dflist[i].reset_index(drop=True, inplace=True)
  # combine columns wanted into one df, for each MDR
  mdr_cases = list(dflist[0].columns)
  all_MDR_across_run = []
  for i in range(len(mdr_cases)):
    all_MDR_across_run.append(pd.DataFrame(columns = range(241))) # 241 rows of data are in output file
  for onerun in dflist:
    for i in range(len(mdr_cases)):
      all_MDR_across_run[i] = all_MDR_across_run[i].append(onerun[mdr_cases[i]], ignore_index=True)
  # calculate 90% CI and IQR
  all_MDR_IQR = []
  for i in range(len(mdr_cases)):
    all_MDR_IQR.append(all_MDR_across_run[i].astype('float').quantile([.05, .25, .5, .75, .95]).values.tolist())
  # plot
  for i in range(len(mdr_cases)):
    mdr_case = mdr_cases[i]
    # only plot double-resistant types
    if mdr_case[0:1] == '2':
      color = coloring_legend(mdr_case, option)
      ax.plot(REPORTDAYS, all_MDR_IQR[i][2], label=mdr_case, 
                      color=color)
      ax.fill_between(REPORTDAYS, all_MDR_IQR[i][1], all_MDR_IQR[i][3], 
                      color=color, alpha=0.25)
      if IQR_only == False:
        ax.fill_between(REPORTDAYS, all_MDR_IQR[i][0], all_MDR_IQR[i][4], 
                        color=color, alpha=0.1)
    
  # Mark where it exceeds the 1% and 10% for most-dangerous type
  idx_one_percent = -1
  idx_ten_percent = -1
  for idx,val in enumerate(all_MDR_IQR[-1][2]):
    if val > 0.01:
      idx_one_percent = idx
      break
  for idx,val in enumerate(all_MDR_IQR[-1][2]):
    if val > 0.1:
      idx_ten_percent = idx
      break
  if idx_one_percent != -1:
    ax.plot(REPORTDAYS[idx_one_percent], all_MDR_IQR[-1][2][idx_one_percent], 'o', color='k')
    t_01 = round(REPORTDAYS[idx_one_percent]/365-10, 1)
  else:
    t_01 = 'N/A'
  if idx_ten_percent != -1:
    ax.plot(REPORTDAYS[idx_ten_percent], all_MDR_IQR[-1][2][idx_ten_percent], 'o', color='k')

  if annoty is not None:    
    # for most-dangerous double
    # calculate genotype freq at last day
    x_20 = all_MDR_IQR[-1][2][-1]
    x_20 = round(x_20, 3)
    # calculate area under median curve
    auc = np.trapz(all_MDR_IQR[-1][2], x=REPORTDAYS)
    auc = round(auc, 2)
    # lower quartile
    auc_l = np.trapz(all_MDR_IQR[-1][1], x=REPORTDAYS)
    auc_l = round(auc_l, 2)
    # upper quartile
    auc_u = np.trapz(all_MDR_IQR[-1][3], x=REPORTDAYS)
    auc_u = round(auc_u, 2)

    # annotate
    annotation_string = r"$x_{20}$ = %s" % x_20
    annotation_string += "\n"
    annotation_string += r"$T_{.01}$ = %s" % t_01
    annotation_string += "\n"
    annotation_string += "AUC = %s (%s-%s)" % (auc, auc_l, auc_u)
    ax.text(ANNOTATION_X_LOCATION, annoty*0.78, annotation_string, verticalalignment='top', size=14)
    
# need 100 simulation data for each strategy, as dataframe
# `m` stands for MFT
# `c` stands for 5-Year Cycling
# `a` stands for Adaptive Cycling
# `option` controls plotting function to 
# use regex (dangerous triples) or drug x-x pattern (dangerous doubles)
def fig3_dangerous_triple_or_double_AUC_IQR(ax, m, c, a, pattern, option):
  from plot_helper import calculate_AUC_from_dflist_for_dangerous_triple, \
                          calculate_AUC_from_dflist_for_dangerous_double
  labels = ['MFT', '5-Year Cycling', 'Adaptive Cycling']

  # calculate 90% CI and IQR, for all 3 strategies
  if option == 'triple':
    AUCs_m = calculate_AUC_from_dflist_for_dangerous_triple(m, pattern)
    AUCs_c = calculate_AUC_from_dflist_for_dangerous_triple(c, pattern)
    AUCs_a = calculate_AUC_from_dflist_for_dangerous_triple(a, pattern)
  elif option == 'double':
    AUCs_m = calculate_AUC_from_dflist_for_dangerous_double(m, pattern)
    AUCs_c = calculate_AUC_from_dflist_for_dangerous_double(c, pattern)
    AUCs_a = calculate_AUC_from_dflist_for_dangerous_double(a, pattern)
  else:
    raise ValueError("Invalid option provided in argument.")

  all_data = [AUCs_m, AUCs_c, AUCs_a]
  # rectangular box plot
  bplot = ax.boxplot(all_data,
                     vert=False,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     showfliers=False, # just show IQR and 90% range 
                     medianprops=dict(color='k'), # black median line 
                     labels=labels)  # will be used to label x-ticks
  
  colors = ['#cadab0', '#a6cfd8', '#d1a29b'] # green, blue, coral
  for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

def fig3_dangerous_five_combined_AUC_IQR(ax, m, c, a):
  from plot_helper import calculate_AUC_from_dflist_for_dangerous_triple, \
                          calculate_AUC_from_dflist_for_dangerous_double
  labels = ['MFT', '5-Year Cycling', 'Adaptive Cycling']

  # type 1 - 'TYY..Y2.'
  AUCs_m1 = np.array(calculate_AUC_from_dflist_for_dangerous_triple(m, 'TYY..Y2.'))
  AUCs_c1 = np.array(calculate_AUC_from_dflist_for_dangerous_triple(c, 'TYY..Y2.'))
  AUCs_a1 = np.array(calculate_AUC_from_dflist_for_dangerous_triple(a, 'TYY..Y2.'))
  # type 2 - 'TYY..Y2.'
  AUCs_m2 = np.array(calculate_AUC_from_dflist_for_dangerous_triple(m, 'KNF..Y2.'))
  AUCs_c2 = np.array(calculate_AUC_from_dflist_for_dangerous_triple(c, 'KNF..Y2.'))
  AUCs_a2 = np.array(calculate_AUC_from_dflist_for_dangerous_triple(a, 'KNF..Y2.'))
  # type 3 - wrt DHA-PPQ
  AUCs_m3 = np.array(calculate_AUC_from_dflist_for_dangerous_double(m, 'DHA-PPQ'))
  AUCs_c3 = np.array(calculate_AUC_from_dflist_for_dangerous_double(c, 'DHA-PPQ'))
  AUCs_a3 = np.array(calculate_AUC_from_dflist_for_dangerous_double(a, 'DHA-PPQ'))
  # type 4 - wrt ASAQ
  AUCs_m4 = np.array(calculate_AUC_from_dflist_for_dangerous_double(m, 'ASAQ'))
  AUCs_c4 = np.array(calculate_AUC_from_dflist_for_dangerous_double(c, 'ASAQ'))
  AUCs_a4 = np.array(calculate_AUC_from_dflist_for_dangerous_double(a, 'ASAQ'))
  # type 5 - wrt AL
  AUCs_m5 = np.array(calculate_AUC_from_dflist_for_dangerous_double(m, 'AL'))
  AUCs_c5 = np.array(calculate_AUC_from_dflist_for_dangerous_double(c, 'AL'))
  AUCs_a5 = np.array(calculate_AUC_from_dflist_for_dangerous_double(a, 'AL'))

  AUCs_m = AUCs_m1 + AUCs_m2 + AUCs_m3 + AUCs_m4 + AUCs_m5
  AUCs_c = AUCs_c1 + AUCs_c2 + AUCs_c3 + AUCs_c4 + AUCs_c5
  AUCs_a = AUCs_a1 + AUCs_a2 + AUCs_a3 + AUCs_a4 + AUCs_a5

  all_data = [AUCs_m, AUCs_c, AUCs_a]
  # rectangular box plot
  bplot = ax.boxplot(all_data,
                     vert=False,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     showfliers=False, # just show IQR and 90% range 
                     medianprops=dict(color='k'), # black median line 
                     labels=labels)  # will be used to label x-ticks
  
  colors = ['#cadab0', '#a6cfd8', '#d1a29b'] # green, blue, coral
  for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
  return all_data
