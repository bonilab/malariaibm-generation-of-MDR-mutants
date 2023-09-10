def fig_a_median_trend(ax, fdir_path, act_name, range_95=True, triangle_marker='on'):
  import os
  import pandas as pd
  import numpy as np
  from constants import HEADER_NAME, \
    ENCODINGDB, ENCODING_TO_MN_DICT, \
    REPORTDAYS, FIRST_ROW_AFTER_BURNIN
  from plot_helper import calc_after_burin_auc_from_list, coloring_legend
  assert(act_name in ['DHA-PPQ', 'ASAQ', 'AL'])
  most_dang_double_type = '2-2' if act_name == 'DHA-PPQ' else '2-4'
  df_list = []
  for i in range(1,101):
    df = pd.read_csv(
      os.path.join(fdir_path, f'monthly/{i}.txt'),
      index_col=False,
      names=HEADER_NAME,
      sep='\t'
    ).fillna(0)
    assert df.shape == (361, 283)
    # TODO: assert reported yyyy-mm-dd is the same as expected
    renamed_df = df.filter(items=ENCODINGDB).rename(columns=ENCODING_TO_MN_DICT[act_name])
    renamed_df = renamed_df.groupby(renamed_df.columns, axis=1).sum()
    df_list.append(renamed_df)
  for col in df_list[0].columns:
    targeted_sum_genofreq_100runs = []
    for onedf in df_list:
      targeted_sum_genofreq_100runs.append(onedf[col])
    median_genofreq = np.percentile(targeted_sum_genofreq_100runs, 50, axis=0)
    col_color = coloring_legend(col, option=1)
    ax.plot( # median
      REPORTDAYS[FIRST_ROW_AFTER_BURNIN:], 
      median_genofreq[FIRST_ROW_AFTER_BURNIN:], 
      color=col_color
    )
    ax.fill_between( # IQR
      REPORTDAYS[FIRST_ROW_AFTER_BURNIN:], 
      np.percentile(targeted_sum_genofreq_100runs, 25, axis=0)[FIRST_ROW_AFTER_BURNIN:],
      np.percentile(targeted_sum_genofreq_100runs, 75, axis=0)[FIRST_ROW_AFTER_BURNIN:], 
      color=col_color, alpha=0.25
    )
    if range_95:
      ax.fill_between( # 95% range
        REPORTDAYS[FIRST_ROW_AFTER_BURNIN:], 
        np.percentile(targeted_sum_genofreq_100runs, 2.5, axis=0)[FIRST_ROW_AFTER_BURNIN:], 
        np.percentile(targeted_sum_genofreq_100runs, 97.5, axis=0)[FIRST_ROW_AFTER_BURNIN:], 
        color=col_color, alpha=0.1
      )
    if col == most_dang_double_type:
      # calculate AUC IQR
      auc_100runs = np.apply_along_axis(calc_after_burin_auc_from_list, 1, targeted_sum_genofreq_100runs)
      # find T01 and T1 for most dangerous double
      t_0p01_idx = np.argmax(median_genofreq>=0.01)
      t_0p1_idx = np.argmax(median_genofreq>=0.1)
      if t_0p01_idx != 0:
        ax.plot(REPORTDAYS[t_0p01_idx], median_genofreq[t_0p01_idx], 'o', color='k')
      if t_0p1_idx != 0:
        ax.plot(REPORTDAYS[t_0p1_idx], median_genofreq[t_0p1_idx], 'o', color='k')
    if triangle_marker == 'on' and most_dang_double_type == '2-4' and col == '2-2':
      # find T01 and T1 for '2-2' double
      t_0p01_idx = np.argmax(median_genofreq>=0.01)
      t_0p1_idx = np.argmax(median_genofreq>=0.1)
      if t_0p01_idx != 0:
        ax.plot(REPORTDAYS[t_0p01_idx], median_genofreq[t_0p01_idx], '^', color='k')
      if t_0p1_idx != 0:
        ax.plot(REPORTDAYS[t_0p1_idx], median_genofreq[t_0p1_idx], '^', color='k')

def fig_a_individual_runs(ax, fdir_path, act_name):
  from constants import HEADER_NAME, \
    ENCODINGDB, ENCODING_TO_MN_DICT, \
    REPORTDAYS, FIRST_ROW_AFTER_BURNIN
  import pandas as pd
  import os
  if act_name == 'DHA-PPQ':
    most_dang_double_type = '2-2'
    color = '#fc9272'
  else:
    most_dang_double_type = '2-4'
    color = '#99000d'
  assert(act_name in ['DHA-PPQ', 'ASAQ', 'AL'])
  for i in range(1,101):
    df = pd.read_csv(
      os.path.join(fdir_path, f'monthly/{i}.txt'),
      index_col=False,
      names=HEADER_NAME,
      sep='\t'
    ).fillna(0)
    assert df.shape == (361, 283)
    renamed_df = df.filter(items=ENCODINGDB).rename(columns=ENCODING_TO_MN_DICT[act_name])
    renamed_df = renamed_df.groupby(renamed_df.columns, axis=1).sum()
    ax.plot(
      REPORTDAYS[FIRST_ROW_AFTER_BURNIN:],
      renamed_df[most_dang_double_type][FIRST_ROW_AFTER_BURNIN:],
      color=color, alpha=0.1  
    )

def plot_fig_a_for_one_set(fpath_contains_ac_strategy, fpath_contains_alt_ac_strategy, savepath=''):
  from plot_helper import xaxis_label_ticker
  import matplotlib.ticker as ticker
  import matplotlib.pyplot as plt
  from constants import TITLE_FONTSIZE
  TITLE_FONTSIZE = TITLE_FONTSIZE - 3
  assert(fpath_contains_ac_strategy[-4:] == '_ac/')
  assert(fpath_contains_alt_ac_strategy[-4:] == '_ac/')
  xlocator = 5*365
  ticks_x = xaxis_label_ticker()
  fig, axes = plt.subplots(4, 2, sharex='col', sharey='row',
                          gridspec_kw={'hspace': 0, 'wspace': 0})
  fig.patch.set_facecolor('white')
  (ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8) = axes

  fig_a_median_trend(ax1, fpath_contains_ac_strategy, 'DHA-PPQ')
  fig_a_individual_runs(ax2, fpath_contains_ac_strategy, 'DHA-PPQ')
  fig_a_median_trend(ax3, fpath_contains_ac_strategy, 'ASAQ')
  fig_a_individual_runs(ax4, fpath_contains_ac_strategy, 'ASAQ')
  fig_a_median_trend(ax5, fpath_contains_ac_strategy, 'AL')
  fig_a_individual_runs(ax6, fpath_contains_ac_strategy, 'AL')
  fig_a_median_trend(ax7, fpath_contains_alt_ac_strategy, 'AL')
  fig_a_individual_runs(ax8, fpath_contains_alt_ac_strategy, 'AL')

  ax1.set_title('Median (IQR) genotype frequencies \nfor drug-sensitive (green), \n' 
              +'single-resistant (blue), and \ndouble-resistant (red) genotypes', 
              fontsize=TITLE_FONTSIZE, pad=20)
  ax2.set_title('Individual genotypes trajectories \nof most-resistant double-resistants', 
                fontsize=TITLE_FONTSIZE, pad=20)
  ax7.set_xlabel('Year', fontsize=TITLE_FONTSIZE)
  ax8.set_xlabel('Year', fontsize=TITLE_FONTSIZE)
  for ax in axes:
    ax[0].set_ylim(-0.05, 1.05)
    ax[1].set_ylim(-0.05, 1.05)
  # change font size on x- and y-axis
  for row in axes:
    for ax in row:
      ax.set_ylim(-0.05, 1.05)
      ax.tick_params(axis='x', labelsize=13)
      ax.tick_params(axis='y', labelsize=13)
  fig.add_subplot(111, frameon=False)
  # hide tick and tick label of the big axis
  plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
  # add common x- and y-labels
  plt.ylabel('Genotype Frequency', fontsize=TITLE_FONTSIZE, labelpad=15)
  ax5.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
  ax5.xaxis.set_major_formatter(ticks_x)
  ax6.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
  ax6.xaxis.set_major_formatter(ticks_x)
  if savepath != '':
    plt.savefig(fname=savepath, format='svg', bbox_inches='tight')
  plt.show()

def fig_b_plot_annotator(ax, x_20, t_0p01_idx, auc, ntf, annoty):
  from constants import REPORTDAYS, ANNOTATION_X_LOCATION
  annot_string = r'$x_{20}$ = %s' % round(x_20, 3)
  annot_string += '\n'
  if t_0p01_idx == 0: annot_string += r'$T_{.01}$ = N/A'
  else:
    t_0p01_year_after_burn_in = round((REPORTDAYS[t_0p01_idx] / 365 - 10), 1)
    annot_string += r'$T_{.01}$ = %s' % round(t_0p01_year_after_burn_in, 3)
  annot_string += '\n'
  auc_median, auc_lq, auc_uq = auc
  annot_string += f'AUC = {auc_median:.2f} ({auc_lq:.2f}-{auc_uq:.2f})'
  annot_string += '\n'
  if ntf is not None: annot_string += ntf
  annot_string += '\n'
  ax.text(ANNOTATION_X_LOCATION, annoty*0.90, annot_string, verticalalignment='top', size=14)

def fig_b_dangerous_triple(ax, fdir_path, targeted_regex_pattern, range_95=True, annoty=None): 
  from plot_helper import ntf_string_prep
  import numpy as np
  import pandas as pd
  import os
  from constants import HEADER_NAME, \
    REPORTDAYS, FIRST_ROW_AFTER_BURNIN
  from plot_helper import calc_after_burin_auc_from_list
  ntf = None
  targeted_sum_genofreq_100runs = []
  for i in range(1,101):
    df = pd.read_csv(
      os.path.join(fdir_path, f'monthly/{i}.txt'),
      index_col=False,
      names=HEADER_NAME,
      sep='\t'
    ).fillna(0)
    assert df.shape == (361, 283)
    targeted_sum_genofreq_100runs.append(df.filter(regex=targeted_regex_pattern, axis=1).sum(axis=1).values)
  targeted_sum_genofreq_100runs = np.array(targeted_sum_genofreq_100runs)
  auc_100runs = np.apply_along_axis(calc_after_burin_auc_from_list, 1, targeted_sum_genofreq_100runs)
  if targeted_regex_pattern == r'^TYY..Y2.$':
    ntf = ntf_string_prep(fdir_path, range_95)
  targeted_sum_median_trend = np.percentile(targeted_sum_genofreq_100runs, 50, axis=0)
  ax.plot( # median
    REPORTDAYS[FIRST_ROW_AFTER_BURNIN:], 
    targeted_sum_median_trend[FIRST_ROW_AFTER_BURNIN:], 
    color='#800080'
  )
  ax.fill_between( # IQR
    REPORTDAYS[FIRST_ROW_AFTER_BURNIN:], 
    np.percentile(targeted_sum_genofreq_100runs, 25, axis=0)[FIRST_ROW_AFTER_BURNIN:], 
    np.percentile(targeted_sum_genofreq_100runs, 75, axis=0)[FIRST_ROW_AFTER_BURNIN:], 
    color='#800080', alpha=0.25
  )
  if range_95:
    ax.fill_between( # 95% range
      REPORTDAYS[FIRST_ROW_AFTER_BURNIN:], 
      np.percentile(targeted_sum_genofreq_100runs, 2.5, axis=0)[FIRST_ROW_AFTER_BURNIN:], 
      np.percentile(targeted_sum_genofreq_100runs, 97.5, axis=0)[FIRST_ROW_AFTER_BURNIN:], 
      color='#800080', alpha=0.1
    )
  t_0p01_idx = np.argmax(targeted_sum_median_trend>=0.01)
  t_0p1_idx = np.argmax(targeted_sum_median_trend>=0.1)
  if t_0p01_idx != 0:
    ax.plot(REPORTDAYS[t_0p01_idx], targeted_sum_median_trend[t_0p01_idx], 'o', color='k')
  if t_0p1_idx != 0:
    ax.plot(REPORTDAYS[t_0p1_idx], targeted_sum_median_trend[t_0p1_idx], 'o', color='k')
  auc_median, auc_lq, auc_uq = np.percentile(auc_100runs, [50, 25, 75])
  if annoty is not None:
    fig_b_plot_annotator(
      ax, 
      x_20=targeted_sum_median_trend[-1], 
      t_0p01_idx=t_0p01_idx, 
      auc=[auc_median, auc_lq, auc_uq], 
      ntf=ntf,
      annoty=annoty
    )

def fig_b_dangerous_double(ax, fdir_path, act_name, range_95=True, annoty=None):
  import numpy as np
  import pandas as pd
  import os
  from plot_helper import coloring_legend
  from constants import ENCODINGDB, HEADER_NAME, \
    REPORTDAYS, FIRST_ROW_AFTER_BURNIN, \
    ENCODING_TO_MN_DICT
  from plot_helper import calc_after_burin_auc_from_list
  most_dang_double_type = '2-2' if act_name == 'DHA-PPQ' else '2-4'
  assert(act_name in ['DHA-PPQ', 'ASAQ', 'AL'])
  df_list = []
  for i in range(1,101):
    df = pd.read_csv(
      os.path.join(fdir_path, f'monthly/{i}.txt'),
      index_col=False,
      names=HEADER_NAME,
      sep='\t'
    ).fillna(0)
    assert df.shape == (361, 283)
    renamed_df = df.filter(items=ENCODINGDB).rename(columns=ENCODING_TO_MN_DICT[act_name])
    renamed_df = renamed_df.groupby(renamed_df.columns, axis=1).sum()
    df_list.append(renamed_df.filter(regex=r'^2-.$', axis=1))
  column_names = df_list[0].columns
  for col in column_names:
    targeted_sum_genofreq_100runs = []
    for onedf in df_list:
      targeted_sum_genofreq_100runs.append(onedf[col])
    median_genofreq = np.percentile(targeted_sum_genofreq_100runs, 50, axis=0)
    col_color = coloring_legend(col, option=1)
    ax.plot( # median
      REPORTDAYS[FIRST_ROW_AFTER_BURNIN:], 
      median_genofreq[FIRST_ROW_AFTER_BURNIN:], 
      color=col_color
    )
    ax.fill_between( # IQR
      REPORTDAYS[FIRST_ROW_AFTER_BURNIN:], 
      np.percentile(targeted_sum_genofreq_100runs, 25, axis=0)[FIRST_ROW_AFTER_BURNIN:],
      np.percentile(targeted_sum_genofreq_100runs, 75, axis=0)[FIRST_ROW_AFTER_BURNIN:], 
      color=col_color, alpha=0.25
    )
    if range_95:
      ax.fill_between( # 95% range
        REPORTDAYS[FIRST_ROW_AFTER_BURNIN:], 
        np.percentile(targeted_sum_genofreq_100runs, 2.5, axis=0)[FIRST_ROW_AFTER_BURNIN:], 
        np.percentile(targeted_sum_genofreq_100runs, 97.5, axis=0)[FIRST_ROW_AFTER_BURNIN:], 
        color=col_color, alpha=0.1
      )
    if col == most_dang_double_type:
      # calculate AUC IQR
      auc_100runs = np.apply_along_axis(calc_after_burin_auc_from_list, 1, targeted_sum_genofreq_100runs)
      auc_median, auc_lq, auc_uq = np.percentile(auc_100runs, [50, 25, 75])
      x_20 = median_genofreq[-1]
      # find T01 and T1 for most dangerous double
      t_0p01_idx = np.argmax(median_genofreq>=0.01)
      t_0p1_idx = np.argmax(median_genofreq>=0.1)
      if t_0p01_idx != 0:
        ax.plot(REPORTDAYS[t_0p01_idx], median_genofreq[t_0p01_idx], 'o', color='k')
      if t_0p1_idx != 0:
        ax.plot(REPORTDAYS[t_0p1_idx], median_genofreq[t_0p1_idx], 'o', color='k')
  if annoty is not None:
    fig_b_plot_annotator(
      ax, 
      x_20=x_20, 
      t_0p01_idx=t_0p01_idx, 
      auc=[auc_median, auc_lq, auc_uq], 
      ntf=None,
      annoty=annoty
    )
    # TODO - assert each row sum-up to 1 or 0
    # list(set(mylist)); == [0,1] or == [1,0]

def plot_fig_b_for_one_set(fpath_contains_three_strategies, savepath='', figtitle='off'): 
  from plot_helper import xaxis_label_ticker
  import matplotlib.ticker as ticker
  import matplotlib.pyplot as plt
  from constants import TITLE_FONTSIZE, XLABEL_FONTSIZE, YLABEL_PADDING
  assert(fpath_contains_three_strategies[-1] != '/')
  fpath_monthly_mft = fpath_contains_three_strategies + '_m/'
  fpath_monthly_5yc = fpath_contains_three_strategies + '_c/'
  fpath_monthly_ac = fpath_contains_three_strategies + '_ac/'

  xlocator = 5*365
  ticks_x = xaxis_label_ticker()
  
  # Test plot to get first three rows
  # aligned on y-limits
  fig, axes = plt.subplots(5, 3, sharex='col', sharey='row',
                          gridspec_kw={'hspace': 0, 'wspace': 0})
  (ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9), \
        (ax10, ax11, ax12), (ax13, ax14, ax15) = axes

  #  MFT
  fig_b_dangerous_triple(ax1, fpath_monthly_mft, r'^TYY..Y2.$')
  fig_b_dangerous_triple(ax4, fpath_monthly_mft, r'^KNF..Y2.$')
  fig_b_dangerous_double(ax7, fpath_monthly_mft, 'DHA-PPQ')
  fig_b_dangerous_double(ax10, fpath_monthly_mft, 'ASAQ')
  fig_b_dangerous_double(ax13, fpath_monthly_mft, 'AL')
  #  Cycling
  fig_b_dangerous_triple(ax2, fpath_monthly_5yc, r'^TYY..Y2.$')
  fig_b_dangerous_triple(ax5, fpath_monthly_5yc, r'^KNF..Y2.$')
  fig_b_dangerous_double(ax8, fpath_monthly_5yc, 'DHA-PPQ')
  fig_b_dangerous_double(ax11, fpath_monthly_5yc, 'ASAQ')
  fig_b_dangerous_double(ax14, fpath_monthly_5yc, 'AL')
  #  Adaptive Cycling
  fig_b_dangerous_triple(ax3, fpath_monthly_ac, r'^TYY..Y2.$')
  fig_b_dangerous_triple(ax6, fpath_monthly_ac, r'^KNF..Y2.$')
  fig_b_dangerous_double(ax9, fpath_monthly_ac, 'DHA-PPQ')
  fig_b_dangerous_double(ax12, fpath_monthly_ac, 'ASAQ')
  fig_b_dangerous_double(ax15, fpath_monthly_ac, 'AL')
  (_, row1ylim) = ax1.get_ylim()
  (_, row2ylim) = ax4.get_ylim()
  (_, row3ylim) = ax7.get_ylim()
  (_, row4ylim) = ax10.get_ylim()
  (_, row5ylim) = ax13.get_ylim()
  # TODO - to figure out way to separate the annot part
  # current work-around - draw plot twice
  plt.clf()
  
  lower_row_lim = max(row3ylim, row4ylim, row5ylim)
  lower_row_lowlim = 0 - lower_row_lim * 0.05
  
  fig, axes = plt.subplots(5, 3, sharex='col', sharey='row',
                          gridspec_kw={'hspace': 0, 'wspace': 0})
  fig.patch.set_facecolor('white')
  if figtitle == 'on':
    fig.suptitle(
      'Evolution of Multiple-Drug-Resistant Types', 
      y=0.95, fontweight='bold', fontsize=TITLE_FONTSIZE
    )
  (ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9), \
        (ax10, ax11, ax12), (ax13, ax14, ax15) = axes
  
  #  MFT
  fig_b_dangerous_triple(ax1, fpath_monthly_mft, r'^TYY..Y2.$', annoty=row1ylim)
  fig_b_dangerous_triple(ax4, fpath_monthly_mft, r'^KNF..Y2.$', annoty=row2ylim)
  fig_b_dangerous_double(ax7, fpath_monthly_mft, 'DHA-PPQ', annoty=lower_row_lim)
  fig_b_dangerous_double(ax10, fpath_monthly_mft, 'ASAQ', annoty=lower_row_lim)
  fig_b_dangerous_double(ax13, fpath_monthly_mft, 'AL', annoty=lower_row_lim)
  #  Cycling
  fig_b_dangerous_triple(ax2, fpath_monthly_5yc, r'^TYY..Y2.$', annoty=row1ylim)
  fig_b_dangerous_triple(ax5, fpath_monthly_5yc, r'^KNF..Y2.$', annoty=row2ylim)
  fig_b_dangerous_double(ax8, fpath_monthly_5yc, 'DHA-PPQ', annoty=lower_row_lim)
  fig_b_dangerous_double(ax11, fpath_monthly_5yc, 'ASAQ', annoty=lower_row_lim)
  fig_b_dangerous_double(ax14, fpath_monthly_5yc, 'AL', annoty=lower_row_lim)
  #  Adaptive Cycling
  fig_b_dangerous_triple(ax3, fpath_monthly_ac, r'^TYY..Y2.$', annoty=row1ylim)
  fig_b_dangerous_triple(ax6, fpath_monthly_ac, r'^KNF..Y2.$', annoty=row2ylim)
  fig_b_dangerous_double(ax9, fpath_monthly_ac, 'DHA-PPQ', annoty=lower_row_lim)
  fig_b_dangerous_double(ax12, fpath_monthly_ac, 'ASAQ', annoty=lower_row_lim)
  fig_b_dangerous_double(ax15, fpath_monthly_ac, 'AL', annoty=lower_row_lim)
  ax13.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
  ax13.xaxis.set_major_formatter(ticks_x)
  ax14.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
  ax14.xaxis.set_major_formatter(ticks_x)
  ax15.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
  ax15.xaxis.set_major_formatter(ticks_x)
  ax1.set_title('MFT', fontsize=TITLE_FONTSIZE)
  ax2.set_title('5-Year Cycling', fontsize=TITLE_FONTSIZE)
  ax3.set_title('Adaptive Cycling', fontsize=TITLE_FONTSIZE)
  ax13.set_xlabel('Year', fontsize=TITLE_FONTSIZE)
  ax14.set_xlabel('Year', fontsize=TITLE_FONTSIZE)
  ax15.set_xlabel('Year', fontsize=TITLE_FONTSIZE)
  
  ax7.set_ylim(lower_row_lowlim, lower_row_lim)
  ax8.set_ylim(lower_row_lowlim, lower_row_lim)
  ax9.set_ylim(lower_row_lowlim, lower_row_lim)
  ax10.set_ylim(lower_row_lowlim, lower_row_lim)
  ax11.set_ylim(lower_row_lowlim, lower_row_lim)
  ax12.set_ylim(lower_row_lowlim, lower_row_lim)
  ax13.set_ylim(lower_row_lowlim, lower_row_lim)
  ax14.set_ylim(lower_row_lowlim, lower_row_lim)
  ax15.set_ylim(lower_row_lowlim, lower_row_lim)
  
  fig.add_subplot(111, frameon=False)
  plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
  plt.ylabel('Genotype Frequency', fontsize=TITLE_FONTSIZE, labelpad=15)
  
  ax3.yaxis.set_label_position("right")
  ax3.set_ylabel(
    'DHA-PPQ, AQ\ntriple-resistant',
    rotation=0, 
    fontsize=XLABEL_FONTSIZE, 
    labelpad=YLABEL_PADDING
  )
  ax6.yaxis.set_label_position("right")
  ax6.set_ylabel(
    'DHA-PPQ, LUM\ntriple-resistant',
    rotation=0, 
    fontsize=XLABEL_FONTSIZE, 
    labelpad=YLABEL_PADDING
  )
  ax9.yaxis.set_label_position("right")
  ax9.set_ylabel(
    'DHA-PPQ\ndouble-resistant',
    rotation=0, 
    fontsize=XLABEL_FONTSIZE, 
    labelpad=YLABEL_PADDING
  )
  ax12.yaxis.set_label_position("right")
  ax12.set_ylabel(
    'ASAQ\ndouble-resistant',
    rotation=0, 
    fontsize=XLABEL_FONTSIZE, 
    labelpad=YLABEL_PADDING
  )
  ax15.yaxis.set_label_position("right")
  ax15.set_ylabel(
    'AL\ndouble-resistant',
    rotation=0, 
    fontsize=XLABEL_FONTSIZE, 
    labelpad=YLABEL_PADDING
  )
  if savepath != '':
    plt.savefig(fname=savepath, format='svg', bbox_inches='tight')
  plt.show()

def fig_c_auc_calculation(fdir_path, label, verbose='on'):
  from constants import HEADER_NAME, ALL_TARGETED_5_TYPES_SET
  from plot_helper import calc_after_burin_auc_from_list
  import numpy as np
  import pandas as pd
  import os
  auc_100runs = []
  for i in range(1,101):
    df = pd.read_csv(
      os.path.join(fdir_path, f'monthly/{i}.txt'),
      index_col=False,
      names=HEADER_NAME,
      sep='\t'
    ).fillna(0)
    assert df.shape == (361, 283)
    summed_genofreq = df.filter(items=ALL_TARGETED_5_TYPES_SET).sum(axis=1).values
    auc_100runs.append(calc_after_burin_auc_from_list(summed_genofreq))
  llq,lq,median,uq,uuq = np.percentile(auc_100runs, [2.5,25,50,75,97.5])
  box_one_strategy = {
    'label' : label,
    'whislo': llq,
    'q1'    : lq,
    'med'   : median,
    'q3'    : uq,
    'whishi': uuq,
    'fliers': []    
  }
  if verbose == 'on': # print out results
    print('{:7.2f} ({:7.2f}-{:7.2f})'.format(median, lq, uq))
  return auc_100runs, box_one_strategy
