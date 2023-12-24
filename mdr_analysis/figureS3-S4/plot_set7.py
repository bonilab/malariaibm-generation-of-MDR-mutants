import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import MaxNLocator



# Load the dataset
df = pd.read_csv('./Set7.csv')

# Define the metric groups based on the column names in the dataset
metric_groups = [
    ['AUC_LQ_DHA-PPQ-AQ-triple','AUC_Med_DHA-PPQ-AQ-triple', 'AUC_UQ_DHA-PPQ-AQ-triple'],
    # ['AUC_LQ_DHA-PPQ-LUM-triple', 'AUC_Med_DHA-PPQ-LUM-triple','AUC_UQ_DHA-PPQ-LUM-triple'], 
    ['AUC_LQ_DHA-PPQ-double','AUC_Med_DHA-PPQ-double', 'AUC_UQ_DHA-PPQ-double'], 
    ['AUC_LQ_ASAQ-double','AUC_Med_ASAQ-double', 'AUC_UQ_ASAQ-double']
]

scenarios = ['baseline', 'no_184', 'no_mdr1', 'no_184_no_mdr1']

width = 0.02
policy_spacing = 0.2  # Adjust this value to control the spacing between the POLICY groups
policy_positions = [i * (len(scenarios) * width + policy_spacing) for i in range(len(df['POLICY'].unique()))]

fs = 20
light_blue = sns.color_palette("deep")[0]

fig, axes = plt.subplots(nrows=len(metric_groups), ncols=1, figsize=(15, 3*len(metric_groups)), sharex=True)

# Iterate over each metric group
for aa, (lq, med, uq) in enumerate(metric_groups):
    ax = axes[aa]
    
    for j,s in enumerate(scenarios):
        # Plot values for each POLICY within the current metric group
        for idx, policy in enumerate(df['POLICY'].unique()):
            policy_df = df[(df['POLICY'] == policy) & (df['SCENARIO'] == s)]
            ax.errorbar(policy_positions[idx] + j*width, 
                        policy_df[med].mean(), 
                        yerr=[[policy_df[med].mean() - policy_df[lq].mean()], [policy_df[uq].mean() - policy_df[med].mean()]], 
                        fmt='o', color=light_blue, markersize=12, elinewidth=4)

    
    
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4)) 
    ax.tick_params(axis='y', labelsize=fs)
    
    # Setting x-axis ticks and labels
    ax.set_xticks([pos + 1.5*width for pos in policy_positions])
    ax.set_xticklabels(["MFT", "5-year Cycling", "Adaptive Cycling"], fontsize=fs)
    
    # Extracting a representative label from the metric group for the y-label
    ylabel = med.replace("AUC_Med_", "")
    ax.set_ylabel(ylabel, fontsize=fs)
    
    ax.grid(axis='x')

 # Add an invisible axis that spans the entire figure
ax_fake = fig.add_subplot(111, frame_on=False)
ax_fake.yaxis.label.set_fontsize(fs+2)  # Set the font size of the main label
ax_fake.set_ylabel("AUC",labelpad=70)  # Set the main y-label
ax_fake.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)  # Hide ticks
ax_fake.grid(False)  # Hide grid

plt.tight_layout()
plt.show()
