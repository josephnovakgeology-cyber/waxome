# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 15:02:47 2026

@author: joseph novak

Last updated: 10/6/2026

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

"""

import pandas as pd

# Load the dataset
file_path = r"C:\Users\josep\OneDrive\Documents\papers\alkane_biomization\code\plant_data.xlsx"
df = pd.read_excel(file_path)

# Grabbing the columns with the n-alkane frational abundances and concentration data
target_cols = [col for col in df.columns if col.startswith('fC') or col.startswith('conc_')]

# Group the data by taxon name and calculate the mean and standard deviation for each
summary_stats = df.groupby('Taxa')[target_cols].agg(['mean', 'std'])

# Formatting
summary_stats.columns = [f"{col}_{stat}" for col, stat in summary_stats.columns]

# Make sure we did not lost the taxa name
summary_stats = summary_stats.reset_index()

# Grab the pft and number of observations for each taxon
pft_info = df.groupby('Taxa')[['Plant Functional Type 1', 'Plant Functional Type 2']].first().reset_index()
counts_info = df.groupby('Taxa').size().reset_index(name='n_entries')

# Merge into one big dataframe for export
final_summary = pd.merge(pft_info, counts_info, on='Taxa')
final_summary = pd.merge(final_summary, summary_stats, on='Taxa')

# Display the first few rows to make sure nothing went terrible wrong
print(final_summary.head())

# Export to species summary .xlsx file
final_summary.to_excel("species_summary_stats.xlsx", index=False)