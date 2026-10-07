# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 17:23:54 2026

@author: joseph novak

This is the execution script for the Waxome Model. The only arguments that need to be updated to run this script
for data from a different study site are the species_data file path and the sediment_data file path. I also 
recommend updating the study site name argument so that the output files reflect where you are working :p

This script requires the waxome.py script to be in the same folder in order to work. Please see the user guide on 
Github if you are having any issues figuring out how to use this. I am also happy to help if you send me an email.

- JB (joseph_novak@brown.edu)
"""

# Import functions from waxome.py
from waxome import (
    load_waxome_parameterizations, 
    spin_up_waxome, 
    load_in_sediment_samples, 
    waxome_analysis
)

# Functions are called here
if __name__ == "__main__":
    
    # Define file paths
    species_data = r"C:\Users\josep\OneDrive\Documents\papers\alkane_biomization\code\species_summary_stats_with_biomes.xlsx"
    sediment_data = r"baikal_250ka_alkanes.xlsx"

    # Load parameterizations
    alphas, taxa, alkane_chains = load_waxome_parameterizations(species_data)
    
    # Run Monte Carlo simulation
    combined_simulation_results = spin_up_waxome(alphas, taxa, alkane_chains)
    
    # Load sedimentary n-alkane data
    seds = load_in_sediment_samples(sediment_data, alkane_chains)
    
    # Run NMF and comprison to Waxome simulations
    waxome_analysis(
        combined_simulation_results, 
        n_NMF_endmembers=2, 
        sediment_file=sediment_data, 
        study_site='Lake Baikal',
        angle=25
    )