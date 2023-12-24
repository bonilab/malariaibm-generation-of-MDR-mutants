# -*- coding: utf-8 -*-


#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load the dataset
df = pd.read_csv('./Set11_AUC_triple_res.csv')

# Define the metric groups based on the column names in the dataset
metric_groups = [
    ["AUC_LQ_ALtriple", "AUC_Med_ALtriple", "AUC_UQ_ALtriple"],
    ["AUC_LQ_Altriple_NewLumLocus10", "AUC_Med_ALtriple_NewLumLocus10", "AUC_UQ_ALtriple_NewLumLocus10"],
    ["AUC_LQ_Altriple_NewLumLocus20", "AUC_Med_ALtriple_NewLumLocus20", "AUC_UQ_ALtriple_NewLumLocus20"],
    ["AUC_LQ_Altriple_NewLumLocus30", "AUC_Med_ALtriple_NewLumLocus30", "AUC_UQ_ALtriple_NewLumLocus30"]
]

# Setting the positions for POLICY groups on the x-axis
# policy_positions = list(range(len(df['POLICY'].unique())))

width = 0.02
  # offset width for metric groups
# Introducing a new variable to control the spacing between primary POLICY groups
policy_spacing = 0.2  # Adjust this value to control the spacing between the POLICY groups

policy_positions = [i * (len(metric_groups) * width + policy_spacing) for i in range(len(df['POLICY'].unique()))]

fs = 24
plt.figure(figsize=(15, 5))

light_blue = sns.color_palette("deep")[0]


# Iterate over each metric group
for j, (lq, med, uq) in enumerate(metric_groups):
    # Plot values for each POLICY within the current metric group
    for idx, policy in enumerate(df['POLICY'].unique()):
        policy_df = df[df['POLICY'] == policy]
        plt.errorbar(policy_positions[idx] + j*width, 
                     policy_df[med].mean(), 
                     yerr=[[policy_df[med].mean()-policy_df[lq].mean()], [policy_df[uq].mean()-policy_df[med].mean()]], 
                     fmt='o', color=light_blue, markersize=12,elinewidth=4)

plt.yticks(np.linspace(0, 1.8, 4))

# Setting x-axis ticks and labels
plt.xticks(ticks=[pos + 1.5*width for pos in policy_positions], 
           labels=["MFT", "5-year Cycling", "Adaptive Cycling"],
           fontsize=fs)
plt.yticks(fontsize=fs)
plt.ylabel('AUC',fontsize=fs+2)
plt.grid(axis='x')
plt.tight_layout()
plt.show()



