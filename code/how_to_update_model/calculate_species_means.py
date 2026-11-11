# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 15:02:47 2026

@author: joseph novak

Last updated: 11/8/2026

This script creates a .xlsx file with the statistical summaries for each entry in the plant_data.xlsx file. This script is the first step to re-parameterizing the model and 
must be run at any point that you choose to update the plant_data.xlsx file with new measurements or taxa. This is because the model reads the 
"species_summary_stats_with_biomes.xlsx" file, not "plant_data.xlsx"

IMPORTANT: do not make any alterations to the headers in the plant_data.xlsx file. If you do, this code will not work. It assumes you are
using the exact same headers as me. 

Please feel free to send me an email if you run into issues with this script. I am happy to help, and I am really happy that the model
interests you enough that you want to re-parameterize it. I hope it is helpful in your research!

- JB (joseph_novak@brown.edu) 

########### Change log ###############
10/6/2026 - cleaned up the code for initial peer review submission, including line-by-line comments describing what the code is doing. For clarity, the 
            import .xlsx file was renamed to "plant_data.xlsx" to make the file names easier to understand.
            
11/8/2026 - replaced the concentration-MC draw method with the Dirichlet method for taxon draws in Waxome.
            Updated this script accordingly to calculate the needed paramterizations.

"""

import pandas as pd

# Load the dataset
file_path = r"C:\Users\josep\OneDrive\Documents\papers\alkane_biomization\code\github_version\plant_data.xlsx"
df = pd.read_excel(file_path)

# Calculate total concentration
conc_cols = [col for col in df.columns if col.startswith('conc_')]
df['total_conc'] = df[conc_cols].sum(axis=1)

# Grab fractional abundances and total concentration
fc_cols = [col for col in df.columns if col.startswith('fC')]
target_cols = fc_cols + ['total_conc']

# Group the data by taxon and calculate the mean and standard deviation
summary_stats = df.groupby('Taxa')[target_cols].agg(['mean', 'std'])
summary_stats.columns = [f"{col}_{stat}" for col, stat in summary_stats.columns]
summary_stats = summary_stats.reset_index()

# Grab the PFT and number of observations for each taxon
pft_info = df.groupby('Taxa')[['Plant Functional Type 1', 'Plant Functional Type 2']].first().reset_index()
counts_info = df.groupby('Taxa').size().reset_index(name='n_entries')

# Merge into one big dataframe
final_summary = pd.merge(pft_info, counts_info, on='Taxa')
final_summary = pd.merge(final_summary, summary_stats, on='Taxa')

# Calculate values for n=1 occurrences
n_gt_1 = final_summary[final_summary['n_entries'] > 1]

for col in target_cols:
    mean_col = f"{col}_mean"
    std_col = f"{col}_std"
    
    # Calculate median across all well-sampled taxa for this specific property
    median_cv = (n_gt_1[std_col] / (n_gt_1[mean_col] + 1e-9)).median()
    
    # Apply to taxa with one obs. to estimate their standard deviation
    mask_n1 = final_summary['n_entries'] == 1
    final_summary.loc[mask_n1, std_col] = final_summary.loc[mask_n1, mean_col] * median_cv

# Display the first few rows to check our work
print(final_summary.head())

# Export to species summary .xlsx file
final_summary.to_excel("species_summary_stats.xlsx", index=False)