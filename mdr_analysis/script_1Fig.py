#!/usr/bin/env python
# coding: utf-8

# # Fig.1 - Single- and Double-Resistant Genotype Trends (w/ 3x2 subpanels)

def script_fig1_plotter(file_path_adpcyc, file_path_aac, plot_savepath, 
                        IQR_only=False, 
                        TITLE_FONTSIZE=18, XLABEL_FONTSIZE=15, 
                        YLABEL_PADDING = 150):

    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    from constant import REPORTDAYS, HEADER_NAME, COLUMNS_TO_DROP
    from plot_helper import xaxis_label_ticker
    from plotter import fig1_plot_IQR, fig1_plot_vars

    plt.rcParams['figure.figsize'] = [12, 12]
    rc = {"font.family" : "sans-serif", 
          "font.style" : "normal",
          "mathtext.fontset" : "dejavusans"}
    plt.rcParams.update(rc)
    plt.rcParams["font.sans-serif"] = ["Myriad Pro"] + plt.rcParams["font.sans-serif"]

    # Read in all 100 simulations as df to show variations and to compute IQR
    dflist = []
    for i in range(1,101):
      dflist.append(pd.read_csv(file_path_adpcyc % i, index_col=False, names=HEADER_NAME, sep='\t').drop(columns=COLUMNS_TO_DROP))

    dflist_aac = []
    for i in range(1,101):
      dflist_aac.append(pd.read_csv(file_path_aac % i, index_col=False, names=HEADER_NAME, sep='\t').drop(columns=COLUMNS_TO_DROP))

    xlocator = 5*365
    ticks_x = xaxis_label_ticker()

    fig, axs = plt.subplots(4, 2, sharex='col', sharey='row',
                            gridspec_kw={'hspace': 0, 'wspace': 0})
    fig.patch.set_facecolor('white')

    (ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8) = axs

    fig1_plot_IQR(ax1, dflist, 'DHA-PPQ', IQR_only)
    fig1_plot_vars(ax2, dflist, 'DHA-PPQ')
    fig1_plot_IQR(ax3, dflist, 'ASAQ', IQR_only)
    fig1_plot_vars(ax4, dflist, 'ASAQ')
    fig1_plot_IQR(ax5, dflist, 'AL', IQR_only)
    fig1_plot_vars(ax6, dflist, 'AL')
    fig1_plot_IQR(ax7, dflist_aac, 'AL', IQR_only)
    fig1_plot_vars(ax8, dflist_aac, 'AL')

    ax1.set_title('Median (IQR) genotype frequencies \nfor single- and double-resistants', fontsize=TITLE_FONTSIZE)
    ax2.set_title('Individual genotypes trajectories \nof most-resistant double-resistants', fontsize=TITLE_FONTSIZE)

    for ax in axs:
        ax[0].set_ylim(-0.05, 1.05)
        ax[1].set_ylim(-0.05, 1.05)
      
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    # add common x- and y-labels
    plt.xlabel('Year', fontsize=XLABEL_FONTSIZE)
    plt.ylabel('Genotype Frequency', fontsize=XLABEL_FONTSIZE)

    ax5.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
    ax5.xaxis.set_major_formatter(ticks_x)
    ax6.xaxis.set_major_locator(ticker.MultipleLocator(xlocator))
    ax6.xaxis.set_major_formatter(ticks_x)

    ax1.set_ylabel('w.r.t. DHA-PPQ', multialignment='left', 
                   horizontalalignment='left', rotation=0, 
                   fontsize=XLABEL_FONTSIZE, labelpad=YLABEL_PADDING)
    ax3.set_ylabel('w.r.t. ASAQ', multialignment='left', 
                   horizontalalignment='left', rotation=0, 
                   fontsize=XLABEL_FONTSIZE, labelpad=YLABEL_PADDING)
    ax5.set_ylabel('w.r.t. AL', multialignment='left', 
                   horizontalalignment='left', rotation=0, 
                   fontsize=XLABEL_FONTSIZE, labelpad=YLABEL_PADDING)
    ax7.set_ylabel('w.r.t. AL \nbut starting with \nKNY genotypes', 
                   multialignment='left', horizontalalignment='left', 
                   rotation=0, fontsize=XLABEL_FONTSIZE, 
                   labelpad=YLABEL_PADDING)

    plt.savefig(fname=plot_savepath, format='svg')
