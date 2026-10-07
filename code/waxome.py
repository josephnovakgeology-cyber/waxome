# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 10:59:25 2026

@author: joseph novak

Waxome is a proxy model that generates a range of possible n-alkane distributions in sediment based on Polar and Subpolar plant wax distributions.
The code included here defines functions that do four things:
    (1) spins up the model, which consists of running 6,000 Monte Carlo simulations (1 simulation for each biome). These 
        simulations represent the range of landscape-scale n-alkane profiles that the different vegetation from each biome
        could produce based on observations of the n-alkane concentrations of each individual plant.
    
    (2) extracts non-negative matrix factorization (NMF) endmembers from a .xlsx file of C23-C31 odd n-alkanes.
    
    (3) projects the NMF endmembers and sediment samples onto the PCA space of the proxy model simulations. 
    
    (4) calculates the proportion of the simulations for each biome that are within an angular distance of 25° from each NMF endmember. 
        The biomes are then ranked, with the biomes most similar to the NMF endmember having the highest score.

The model has 6 biome types:
    
    1). Tundra
    2). Forest-Steppe
    3). Boreal Forest
    4). Tall Shrub Tundra
    5). Graminoid Dwarf Shrub Tundra
    6). Aquatics
    
The model is based upon the following equation:
    
    species n-alkane distributions x species n-alkane production rate x plant functional type abundance 
    
Each of these terms has its own uncertainty, which is propogated through the model.

The model and its helper functions are defined below. The execution code (execution_code.py) runs these functions. If you are unsure how to use these functions 
or on how to run them within the execution code, please check out the user_guide.md file on Github. It contains a detailed example of how to use the code with the demo
datasets that are included from Lake Baikal, which are the same datasets shown in the Waxome manuscript. There are also detailed notes and annotations in the code
to help explain what everything does.

Thank you for your interest in our work! If you are having trouble getting this all to run, please feel free to reach out to me over email. I am really happy that
you are interested in the proxy model and I will do my best to get you up and running. 

- JB (joseph_novak@brown.edu)

##### Change Log #####
10/6/2026 Working scripts were reformatted into this publication-ready format and tested.

"""
import pandas as pd
import numpy as np
import time
from tqdm import trange
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt


def load_waxome_parameterizations(species_data_file_path, Drichilet_shape_parameter = 20):
    """
    This function loads the data and calculates the parameterizations needed to run Waxome. 

    Parameters
    ----------
    species_data_file_path : string
        The file path to the species_summary_stats_with_biomes.xlsx file on your computer. 
        
    Drichilet_shape_parameter : int, optional
        The shape parameter for the Dirichilet distributions that are built by the spin_up_Waxone function. The default is 20.

    Returns
    -------
    alphas : pandas dataframe 
        containing the alpha parameter to calculate Dirichilet distributions for the PFT abundances within each biome.
        
    taxa : pandas dataframe
        The pandas dataframe that is read in from species_summary_stats_with biomes.xlsx
        
    alkane_chains : pandas dataframe
        The n-alkane relative abundances and concentration data, with estimated uncertainties of +/- 90% for instances of one entry for a taxon.

    """
    taxa = pd.read_excel(species_data_file_path)
    # grab the concentration and relative abundance columns
    alkane_chains = [c.split('_')[1] for c in taxa.columns if c.startswith('conc_') and c.endswith('_mean')]

    # Fill NaN means with 0, and as a standard deviation of +/- 10% for taxa with only one measurement
    for chain in alkane_chains:
        mean_col = f'conc_{chain}_mean'
        std_col = f'conc_{chain}_std'
        
        if mean_col in taxa.columns and std_col in taxa.columns:
            taxa[mean_col] = taxa[mean_col].fillna(0.0)
            taxa[std_col] = taxa[std_col].fillna(taxa[mean_col] * 0.90)
            taxa[std_col] = taxa[std_col].fillna(0.0)

    # Biome-specific PFT abundances and converstion to Drichilet alpha values
    biome_bounds = {
        'Biome': ['Cold Steppe',  "Forest-Steppe", 'Boreal Forest', 'Tall Shrub Tundra', 'Graminoid Dwarf Shrub Tundra', 'Aquatic'],
        'tree': [[0, 0], [0.15, 0.5], [0.70, 0.95], [0, 0.2],  [0, 0], [0, 0]],
        'shrub': [[0, 0.67],  [0.1, 0.7], [0.01, 0.285], [0.40, 0.95],  [0.15, 0.65], [0, 0]],
        'graminoid': [[0, 0.85],  [0.2, 0.6], [0, 0.05], [0.05, 0.1],  [0.5, 0.8], [0, 0]],
        'herb_forb': [[0, 0.9], [0, 0.45],  [0, 0.06], [0, 0.015],  [0, 0.3], [0, 0]],
        'moss_lichen_liverwarts_ferns': [[0, 0.1],  [0, 0.1], [0, 0.18], [0, 0.2], [0.2, 0.7], [0, 0]],
        'aquatic_macrophytes': [[0, 0],  [0, 0],[0, 0], [0, 0],  [0, 0], [0, 1]],
        'algae': [[0, 0],  [0, 0], [0, 0], [0, 0],  [0, 0], [0, 1]]
    }

    df_bounds = pd.DataFrame(biome_bounds).set_index('Biome')
    df_midpoints = df_bounds.map(lambda x: sum(x) / 2.0)
    df_normalized = df_midpoints.div(df_midpoints.sum(axis=1), axis=0)

    S = Drichilet_shape_parameter  
    alphas = (df_normalized * S).replace(0.0, 1e-4)
    return alphas, taxa, alkane_chains


# Defining the sedimentary n-alkane forward model 

def waxome(alphas, taxa, alkane_chains, max_species_per_pft=50):
    """
    Runs one iteration of the Monte Carlo Simulation.
    Calculates biome-specific Plant Functional Type (PFT) signatures 
    before applying the Dirichlet mixing. 
    
    The parameters for this function are the outputs of load_Waxome_parameterizations
    
    Parameters
    ----------
    alphas : pandas dataframe 
        containing the alpha parameter to calculate Dirichilet distributions for the PFT abundances within each biome.
        
    taxa : pandas dataframe
        The pandas dataframe that is read in from species_summary_stats_with biomes.xlsx
        
    alkane_chains : pandas dataframe
        The n-alkane relative abundances and concentration data, with estimated uncertainties of +/- 90% for instances of one entry for a taxon.
    
    Returns
    -------
    biome_final_distributions: pandas dataframe
    This is the outcome of one iteration of the Monte Carlo simulations
    
    """

    
    # Simulating the plants in each biome
    cols_to_keep = ['Taxa', 'Plant Functional Type 1', 'Plant Functional Type 2']
    cols_to_keep = [c for c in cols_to_keep if c in taxa.columns]
    
    # Identify biome columns in the dataset 
    biome_cols = [b for b in alphas.index if b in taxa.columns]
    cols_to_keep.extend(biome_cols)
    
    simulated_taxa = taxa[cols_to_keep].copy()
    
    for chain in alkane_chains:
        mean_col = f'conc_{chain}_mean'
        std_col = f'conc_{chain}_std'
    
        mu = taxa[mean_col].values
        sigma = taxa[std_col].values
    
        # Avoid division by zero for zero-concentration chains
        mask = (mu > 0) & (sigma > 0)
    
        # Initialize draws array with zeros
        draw = np.zeros_like(mu)
    
        if np.any(mask):
            # Calculate Log-Normal parameters for non-zero entries
            var_log = np.log(1 + (sigma[mask]**2 / mu[mask]**2))
            sigma_log = np.sqrt(var_log)
            mu_log = np.log(mu[mask]) - (var_log / 2.0)
        
            # Draw from Log-Normal distribution
            draw[mask] = np.random.lognormal(mean=mu_log, sigma=sigma_log)
        
        simulated_taxa[chain] = draw
        
    pft_cols = [c for c in ['Plant Functional Type 1', 'Plant Functional Type 2'] if c in simulated_taxa.columns]
    
    # combine information in PFT 1 and PFT 2
    melted_taxa = simulated_taxa.melt(
        id_vars=['Taxa'] + alkane_chains + biome_cols, 
        value_vars=pft_cols, 
        value_name='Assigned_PFT'
    )
    
    valid_pfts = alphas.columns.tolist()
    melted_taxa = melted_taxa[melted_taxa['Assigned_PFT'].isin(valid_pfts)]
    
    biome_final_distributions = {}
    
    for biome in alphas.index:
        # Filter for taxa actually present in this specific biome
        if biome in melted_taxa.columns:
            biome_taxa = melted_taxa[melted_taxa[biome] == 1]
        else:
            biome_taxa = melted_taxa 
            
        # Draw up to `max_species_per_pft` with replacement for each PFT in this biome
        pft_signatures_list = []
        for pft, group in biome_taxa.groupby('Assigned_PFT'):
            sampled_group = group.sample(n=max_species_per_pft, replace=True)
            mean_sig = sampled_group[alkane_chains].mean()
            mean_sig.name = pft
            pft_signatures_list.append(mean_sig)
            
        if pft_signatures_list:
            pft_signatures = pd.DataFrame(pft_signatures_list)
        else:
            pft_signatures = pd.DataFrame(columns=alkane_chains)
        
        # Fill missing PFTs with 0
        for pft in alphas.columns:
            if pft not in pft_signatures.index:
                pft_signatures.loc[pft] = 0.0
                
        pft_signatures = pft_signatures.sort_index()
        
        # Draw the simulated landscape fractions for this biome
        landscape_fractions = np.random.dirichlet(alphas.loc[biome].values)
        landscape_series = pd.Series(landscape_fractions, index=alphas.columns)
        
        # Sort landscape to match PFT rows perfectly
        landscape_series = landscape_series.reindex(pft_signatures.index)
        
        # Calculate absolute wax for this biome (Dot Product)
        biome_absolute_wax = landscape_series.dot(pft_signatures)
        
        # Normalize to fractional abundance
        biome_sum = biome_absolute_wax.sum() + 1e-9
        biome_final_distributions[biome] = biome_absolute_wax / biome_sum
        
    return pd.DataFrame.from_dict(biome_final_distributions, orient='index')

def spin_up_waxome(alphas, taxa, alkane_chains, max_species_per_pft = 50, seed = 265, n_iterations = 1000):
    """
    This function runs the Monte Carlo iterations of Waxome. It requires the outputs from the load_Waxome_parameterization function to run.

    Parameters
    ----------
    alphas : pandas dataframe 
        containing the alpha parameter to calculate Dirichilet distributions for the PFT abundances within each biome.
        
    taxa : pandas dataframe
        The pandas dataframe that is read in from species_summary_stats_with biomes.xlsx
        
    alkane_chains : pandas dataframe
        The n-alkane relative abundances and concentration data, with estimated uncertainties of +/- 90% for instances of one entry for a taxon.
        
    max_species_per_pft : int, optional
        The maximum number of taxa per plant functional type. The default is 50.
        
    seed : int, optional
        Set the seed so that the work is reproducible between runs. The default is 265.
        
    n_iterations : int, optional
        The number of Monte Carlo simulations run for each biome. The default is 1000.

    Returns
    -------
    combined_results : pandas dataframe
        The resulting n-alkane distributions from the Monte Carlo runs.

    """
    np.random.seed(seed)
    n_iterations = n_iterations
    all_simulations = []
    print("Spinning up Waxome...")
    print(f"Running Monte Carlo Simulation ({n_iterations} iterations per biome)...")
    print("This might take a hot second...")
    
    for i in trange(n_iterations):
        iteration_result = waxome(alphas, taxa, alkane_chains, max_species_per_pft)
        all_simulations.append(iteration_result)
    
    combined_simulation_results = pd.concat(all_simulations)
    return combined_simulation_results

def load_in_sediment_samples(sediment_file, alkane_chains):
    """
    This function loads in the sediment sample data and formates the dataframe objects to run in Waxome

    Parameters
    ----------
    sediment_file : string
        File path for the .xlsx file containing the sedimentary n-alkane data
    alkane_chains : pandas dataframe
        The n-alkane relative abundances and concentration data, with estimated uncertainties of +/- 90% for instances of one entry for a taxon. 

    Returns
    -------
    sediments : pandas dataframe
        The loaded-in .xlsx file
    sediment_abundances : pandas dataframe
        n-alkane relative abundances from the sediments file.

    """
    
    sediments = pd.read_excel(sediment_file)

    fractional_columns = [f"f{chain}" for chain in alkane_chains]
    sediment_abundances = sediments[fractional_columns].copy()
    sediment_abundances.columns = alkane_chains
    sediment_abundances = sediment_abundances.div(sediment_abundances.sum(axis=1), axis=0)
    
    return sediments, sediment_abundances
    
def waxome_analysis(combined_simulation_results, n_NMF_endmembers, sediment_file, study_site = "Unknown", angle = 25):
    """
    

    Parameters
    ----------
    combined_simulation_results : pandas dataframe
        Carrying forward the simulation results.
    n_NMF_endmembers : int
        The number of NMF endmembers to be extracted from the sediments. This value should be updated after seeing the Scree plot.
    sediment_file : string
        Carrying forward the sediment data from the above function.
    study_site : string, optional
        Type in the name of your study site so that your plots are named. The default is "Unknown".
    angle : int, optional
        The angular distance threshold for determining the most likely biome. The default is 25.

    Returns
    -------
    Print statement
        The outputs from the analysis are automatically saved to the folder you are working in :)

    """
    alkane_chains = combined_simulation_results.columns.tolist()
    sediments, sediment_abundances = load_in_sediment_samples(sediment_file, alkane_chains)
    
    # calculating the mean n-alkane profile of each biome (the Waxome, if you prefer)
    print("Calculating mean biome n-alkane profiles...")
    final_mean = combined_simulation_results.groupby(combined_simulation_results.index).mean()
    final_std = combined_simulation_results.groupby(combined_simulation_results.index).std()
    biome_order = ['Cold Steppe',  "Forest-Steppe", 'Boreal Forest', 'Tall Shrub Tundra', 'Graminoid Dwarf Shrub Tundra',  'Aquatic']
    final_mean = final_mean.reindex(biome_order)
    final_std = final_std.reindex(biome_order)
    
    print("Conducting PCA on all simulated n-alkane distributions...")
    # PCA on the biome simulations
    X = combined_simulation_results[alkane_chains].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    pca_features = pca.fit_transform(X_scaled)

    df_pca = pd.DataFrame(pca_features, columns=['PC1', 'PC2'])
    df_pca['Biome'] = combined_simulation_results.index.values
    var_exp = pca.explained_variance_ratio_ * 100
    
    # extracting NMF endmembers from the sedimentary n-alkane data
    print("Extracting NMF endmembers from sedimentary n-alkane data...")
    n_endmembers = 2 # Adjusted to match Panel A styling
    nmf = NMF(n_components=n_endmembers, init='nndsvda', random_state=42, max_iter=2000)
    W_weights = nmf.fit_transform(sediment_abundances) 
    H_signatures = nmf.components_                     

    H_normalized = H_signatures / H_signatures.sum(axis=1, keepdims=True)
    df_endmembers = pd.DataFrame(H_normalized, columns=alkane_chains)
    df_endmembers.index = [f"Endmember_{i+1}" for i in range(n_endmembers)]
    
    W_fractional = W_weights / W_weights.sum(axis=1, keepdims=True)

    em_labels = [f'Weight_EM{i+1}' for i in range(n_endmembers)]
    df_weights = pd.DataFrame(W_fractional, columns=em_labels, index=sediments.index)

    df_sample_weights = pd.concat([sediments[['IDs', 'Age (Ka)', 'Depth in Section']], df_weights], axis=1)
    df_sample_weights['Dominant_NMF_Signal'] = df_weights.idxmax(axis=1).str.replace('Weight_', '')

    print("\n--- Fractional NMF Endmember Weights per Sample ---")
    print(df_sample_weights.head(15).round(3))
    df_sample_weights.to_excel(f'{study_site}_NMF_weights_downcore.xlsx', index=False)
    
    # Scree plot to show the variance explained at different numbers of NMF endmembers
    print("Generating NMF Scree Plot...")

    # Evaluate across 1 to N components (limited by total alkane chains)
    max_k = min(6, sediment_abundances.shape[1])
    k_range = range(1, max_k + 1)

    reconstruction_errors = []
    variance_explained = []

    # Calculating the total Frobenius norm squared of the original data matrix
    total_sum_sq = np.sum(sediment_abundances.values ** 2)

    for k in k_range:
        nmf_eval = NMF(n_components=k, init='nndsvda', random_state=42, max_iter=2000)
        nmf_eval.fit(sediment_abundances)
        
        # Reconstruction error = ||X - WH||_F
        rec_err = nmf_eval.reconstruction_err_
        reconstruction_errors.append(rec_err)
        
        # Calculate % variance explained: 1 - (SS_res / SS_tot)
        ss_res = rec_err ** 2
        nmf_var_exp = (1 - (ss_res / total_sum_sq)) * 100
        variance_explained.append(nmf_var_exp)

    # Create Scree Plot
    fig, ax1 = plt.subplots(figsize=(7.5, 4.5))

    # X-Axis: Reconstruction Error
    color_err = '#0072B2'
    ax1.plot(k_range, reconstruction_errors, marker='o', color=color_err, linewidth=2, markersize=7)
    ax1.set_xlabel('Number of NMF Endmembers ($k$)', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Reconstruction Error (Frobenius Norm)', color=color_err, fontweight='bold', fontsize=11)
    ax1.tick_params(axis='y', labelcolor=color_err)
    ax1.set_xticks(k_range)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Y-Axis: Variance Explained (%)
    ax2 = ax1.twinx()
    color_var = '#D55E00'
    ax2.plot(k_range, variance_explained, marker='s', color=color_var, linewidth=2, linestyle='--', markersize=7)
    ax2.set_ylabel('Approx. Variance Explained (%)', color=color_var, fontweight='bold', fontsize=11)
    ax2.tick_params(axis='y', labelcolor=color_var)
    ax2.set_ylim(min(variance_explained) - 5, 102)

    plt.title(f'{study_site} NMF Scree Plot: Model Fit vs. Number of Endmembers', fontweight='bold', fontsize=13)
    fig.tight_layout()

    plt.savefig(f'{study_site}_nmf_scree_plot.pdf', format='pdf', bbox_inches='tight', dpi=300)
    plt.show()
    
    #projecting NMF endmembers onto the simulation PCA space
    print("Projecting NMF endmembers and sediment samples onto the PCA space")
    endmembers_scaled = scaler.transform(df_endmembers.values)
    endmembers_pca = pca.transform(endmembers_scaled)
    df_endmembers['PC1'] = endmembers_pca[:, 0]
    df_endmembers['PC2'] = endmembers_pca[:, 1]
    
    sediment_scaled = scaler.transform(sediment_abundances.values)
    sediment_pca = pca.transform(sediment_scaled)
    
    sediments = pd.DataFrame()
    sediments['PC1'] = sediment_pca[:, 0]
    sediments['PC2'] = sediment_pca[:, 1]
    
    # PCA biplot showing the results of the analysis
    plt.figure(figsize=(10, 7))

    cb_palette = ['#F0E442', '#E69F00', '#009E73', '#CC79A7', '#D55E00', '#0072B2']
    markers = ['o', 's', '^', 'D', 'v', 'p']

    for color, marker, biome in zip(cb_palette, markers, biome_order):
        subset = df_pca[df_pca['Biome'] == biome]
        plt.scatter(subset['PC1'], subset['PC2'], color=color, marker=marker, alpha=0.3, s=15, edgecolor='none')
        plt.scatter(subset['PC1'].mean(), subset['PC2'].mean(), label=biome, color=color, edgecolor='black', linewidth=1.5, s=150, marker=marker, zorder=5)

    # sediment points
    plt.scatter(
        sediments['PC1'], 
        sediments['PC2'],
        color='white',
        marker='*',
        edgecolor='black',
        linewidth=0.5,
        s=100,
        zorder=6  
    )

    # endmember points
    plt.scatter(
        df_endmembers['PC1'], df_endmembers['PC2'],
        marker='X', color='white', edgecolor='black', linewidth=1.5, s=250, label='NMF Endmembers', zorder=10                 
    )
    for i, row in df_endmembers.iterrows():
        em_label = i.replace("Endmember_", "EM") 
        plt.text(row['PC1'] + 0.15, row['PC2'] + 0.15, em_label, fontsize=12, fontweight='bold', zorder=11)

    loadings = pca.components_.T
    scale = np.max(np.abs(pca_features)) * 0.75 
    for i, chain in enumerate(alkane_chains):
        x_val = loadings[i, 0] * scale
        y_val = loadings[i, 1] * scale
        plt.arrow(0, 0, x_val, y_val, color='#4A4A4A', alpha=0.9, width=0.015, head_width=0.15, head_length=0.15, zorder=10)
        plt.text(x_val * 1.15, y_val * 1.15, chain, color='black', weight='bold', fontsize=12, ha='center', va='center', zorder=10)

    plt.axhline(0, color='grey', linestyle='--', alpha=0.5, zorder=1)
    plt.axvline(0, color='grey', linestyle='--', alpha=0.5, zorder=1)
    plt.title(f'PCA of Simulated Biome n-Alkanes vs {study_site} Data', fontweight='bold', fontsize=14)
    plt.xlabel(f'PC1 ({var_exp[0]:.1f}% of Simulation Variance Explained)', fontweight='bold')
    plt.ylabel(f'PC2 ({var_exp[1]:.1f}% of Simulation Variance Explained)', fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.xlim(-4, 4)  
    plt.ylim(-4, 4)  
    plt.legend(title='Biome Endmembers', bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True)
    plt.tight_layout()
    plt.savefig(f'{study_site}_pca_biplot.pdf', format='pdf', bbox_inches='tight')
    plt.show()
    
    
    # Using angular distance to attribute endmembers to specific biomes
    print("\nCalculating angular distances between NMF endmembers and simulated biomes...")

    # Normalize NMF endmember matrix
    em_vals = df_endmembers[alkane_chains].values
    em_norms = np.linalg.norm(em_vals, axis=1, keepdims=True)
    em_unit = em_vals / np.where(em_norms == 0, 1e-9, em_norms)

    attribution_records = []

    # Iterate through each simulated biome
    for biome in combined_simulation_results.index.unique():
        biome_sims = combined_simulation_results.loc[biome, alkane_chains].values
        
        # Normalize simulated compositions
        sim_norms = np.linalg.norm(biome_sims, axis=1, keepdims=True)
        sim_unit = biome_sims / np.where(sim_norms == 0, 1e-9, sim_norms)
        
        # Calculate cosine similarity
        cs_matrix = np.dot(sim_unit, em_unit.T)
        
        # Convert cosine similarity to angulr distance
        ang_dist_matrix = np.degrees(np.arccos(np.clip(cs_matrix, -1.0, 1.0)))
        
        # Evaluate the proportion of each matrix less than of equal to a user-specified
        # angular distance. The defaul is 25°
        for em_idx, em_name in enumerate(df_endmembers.index):
            ang_dists = ang_dist_matrix[:, em_idx]
            
            # Calculate proportion of simulations under specific angular thresholds
            prop = np.mean(ang_dists <= angle)
                        
            attribution_records.append({
                'Endmember': em_name,
                'Biome': biome,
                f'Prop_<={angle}°': prop
            })

    # Export the final matrix with endmember attribution
    df_thresholds = pd.DataFrame(attribution_records)

    # Sort by Endmember, then by the closest match
    df_thresholds.sort_values(
        by=['Endmember', f'Prop_<={angle}°'], 
        ascending=[True, False], 
        inplace=True
    )

    print("\n--- Angular distances of sample endmember from simulated biomes ---")
    print(df_thresholds.round(3).to_string(index=False))

    df_thresholds.to_excel(f'{study_site}_endmember_angular_distance_metrics.xlsx', index=False)
    print("\nSaved angular threshold metrics to 'endmember_angular_distances.xlsx'")
    
    print("Generating bar plots of NMF endmember distributions with attribution...")

    em_chains_only = df_endmembers[alkane_chains]
    n_em = len(em_chains_only)

    em_colors = ['#C475A6', '#E5D94D', '#0072B2', '#D55E00', '#009E73']
    fig, axes = plt.subplots(nrows=n_em, ncols=1, figsize=(6, 2.2 * n_em), sharex=True, sharey=True)

    if n_em == 1:
        axes = [axes]

    y_max_em = max(0.65, em_chains_only.max().max() * 1.15)
    formatted_x_labels = [f"C$_{{{str(c).replace('C', '')}}}$" for c in alkane_chains]

    for i, (ax, em_name) in enumerate(zip(axes, em_chains_only.index)):
        abundances = em_chains_only.loc[em_name]
        color = em_colors[i % len(em_colors)]
        
        ax.bar(
            range(len(alkane_chains)),          
            abundances.values,         
            color=color,     
            edgecolor='black',
            linewidth=1.0,
            width=0.75,
            zorder=3
        )
        
        # Retrieve closest 
        best_match = df_thresholds[df_thresholds['Endmember'] == em_name].iloc[0]
        
        best_biome = best_match['Biome']
        closest = best_match[f'Prop_<={angle}°']*100
        
        label_text = f"NMF {em_name.replace('_', ' ')}\n{closest:.1f}% of {best_biome} \n simulations are within \n {angle}° of this endmember"
        ax.text(
            0.95, 0.88, label_text, 
            transform=ax.transAxes, 
            fontsize=10, 
            ha='right', 
            va='top'
        )

        ax.set_ylim(0, y_max_em)
        ax.set_yticks([0.0, 0.2, 0.4, 0.6])
        ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    fig.supylabel('Fractional Abundance', fontsize=14)
    axes[-1].set_xticks(range(len(alkane_chains)))
    axes[-1].set_xticklabels(formatted_x_labels, fontsize=12)
    axes[-1].set_xlabel('$n$-Alkane Chain Length', fontsize=14)

    plt.tight_layout() 
    plt.savefig(f'{study_site}_nmf_endmember_barplot.pdf', format='pdf', bbox_inches='tight')
    plt.show()
    
    return print('Waxome analysis complete. \n Check your working directory for saved plots and spreadsheets.\n Thanks for using Waxome :)')