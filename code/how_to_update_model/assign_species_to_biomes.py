# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 15:22:49 2026

@author: joseph novak

This script assigns individual plant taxa to different biomes, which is step two of re-parameterizing the model.

Each plant taxa needs to be assigned to a biome for it to be included in the model parameterization. I grouped taxa by 
flouristic assemblages because the biomes should be based on real groups of plants that occur together in nature. 

Be careful to add new plants to these biomes in ecologically realistic ways. This will likely require a bit of reading 
about the preferred habitats of each plant. This is the really labor-intensive part of parameterizing the model
so be careful about changing things up without doing your homework. Things could get weird!

Please feel free to reach out to me if you need help adapting this setup to a new environment or region. I am happy
to help you troubleshoot the code. 

- JB (joseph_novak@brown.edu)
"""

import pandas as pd

# Load the dataset
file_path = r"C:\Users\josep\OneDrive\Documents\papers\alkane_biomization\code\species_summary_stats.xlsx"
df = pd.read_excel(file_path)

# Define the biome lists 
# make sure the names are spelled exactly as in the excel table, otherwise they will not be read properly. 
# improper reading and skipping of taxa is a silent failure, meaning that the script still runs and no error message 
# prints to the console. This is just how the pandas library works, so be careful.

cold_steppe_taxa = [
    # Shrubs & Subshrubs
    "Artemisia sp.", "Artemisia frigida", "Caragana sp.", 
    "Cotoneaster melanocarpus", "Juniperus rigida", "Juniperus cf. davurica", 
    "Lonicera tatarica", "Rosa acicularis", "Salix sp.", "Spiraea media",
    
    # Graminoids (Grasses, Sedges, Rushes) - strictly dry/steppe adapted
    "Calamagrostis lapponica", "Carex scirpoidea", "Cyperaceae", 
    "Leymus chinensis", "Poaceae sp.", "Stipa daicalensis", "Stipa grandis",

    # Herbs & Forbs - dryland/steppe tolerant
    "Campanula rotundifolia", "Cerastium alpinum", 
    
    # Mosses and Lichens 
    "Polytrichum juniperinum", "Polytrichum piliferum", "Racomitrium lanuginosum", 
    "Rhizocarpon cinereovirens", "Rhizocarpon geographicum", "Rhizocarpon geminatum"
]

forest_steppe_taxa = [
    # Boreal Forest Trees
    "Abies nephrolepis", "Alnus viridis", "Betula pendula", 
    "Betula platyphylla", "Betula pubescens", "Larix sp.", "Larix cajanderi", 
    "Larix gmelinii", "Larix laricina", "Larix sibirica", 
    "Picea mariana", "Picea obovata", "Pinus pumila", "Pinus sibirica", 
    "Pinus sylvestris", "Sorbus aucuparia",
    
    # Steppe Shrubs & Subshrubs
    "Artemisia sp.", "Artemisia frigida", "Betula exilis", "Betula fruticosa", 
    "Betula glandulosa", "Caragana sp.", "Cotoneaster melanocarpus", "Juniperus rigida", 
    "Juniperus cf. davurica", "Lonicera tatarica", "Rosa acicularis", "Salix sp.", 
    "Salix alaxensis", "Salix glauca", "Salix pulchra", "Spiraea media",
    
    # Graminoids (Grasses, Sedges, Rushes)
    "Calamagrostis lapponica", "Carex bigelowii", "Carex scirpoidea", 
    "Cyperaceae", "Leymus chinensis", "Poaceae sp.", "Stipa daicalensis", "Stipa grandis",

    # Herbs & Forbs & Ferns
    "Campanula rotundifolia", "Cerastium alpinum", "Chamaenerion latifolium", 
    "Euphrasia wettsteinii", "Woodsia ilvensis",
    
    # Mosses, Lichens, and Liverworts
    "Aulacomnium palustre", "Aulacomnium turgidum", "Hylocomium splendens",
    "Pleurozium schreberi", "Polytrichum juniperinum", "Polytrichum piliferum", 
    "Ptilidium ciliare", "Stereocaulon capitatum", "Stereocaulon sp."
]

boreal_forest_taxa = [
    # Coniferous & Broadleaf Trees
    "Abies nephrolepis", "Abies sibirica", "Alnus viridis", "Betula pendula", 
    "Betula platyphylla", "Betula pubescens", "Larix sp.", "Larix cajanderi", 
    "Larix gmelinii", "Larix laricina", "Larix sibirica",  "Picea mariana", 
    "Picea obovata", "Pinus pumila", "Pinus sibirica", "Pinus sylvestris", "Sorbus aucuparia",

    # Shrubs, Sub-shrubs, and Woody Vines
    "Betula exilis", "Betula fruticosa", "Betula glandulosa", "Betula humilis", "Chamaedaphne calyculata", 
    "Cornus alba", "Cotoneaster melanocarpus", "Lonicera altaica", "Myrica gale", 
    "Oxycoccus microcarpus", "Potentilla fruticosa", "Rhododendron groenlandicum", 
    "Rhododendron sichotense", "Rhododendron tomentosum", "Rosa acicularis", 
    "Salix sp.", "Salix alaxensis", "Salix glauca", "Salix pulchra", "Spiraea media", 
    "Vaccinium myrtillus", "Vaccinium uliginosum", "Vaccinium vitis-idaea",
    
    # Graminoids
    "Carex fuliginosa", "Carex lenticularis", "Carex rostrata", "Carex stylosa", 
    "Cyperaceae", "Eriophorum angustifolium", "Eriophorum vaginatum",
    
    # Herbs & Forbs & Ferns
    "Caltha palustris", "Chamaepericlymenum suecicum", "Chamerion angustifolium", 
    "Comarum palustre", "Cystopteris fragilis", "Cystopteris sp.", 
    "Drosera rotundifolia", "Equisetum arvense", "Polygonum viviparum", 
    "Pyrola grandiflora", "Rubus arcticus", "Rubus chamaemorus", "Rubus saxatilis", 
    "Rumex arcticus", "Scheuchzeria palustris", "Woodsia ilvensis",
    
    # Mosses, Lichens, and Liverworts
    "Anthelia juratzkana", "Aulacomnium palustre", "Calliergon sarmentosum", "Calliergon sp.", 
    "Cephaloziella sp.", "Drepanocladus sp.", "Drepanocladus fluitans",  
    "Hylocomium splendens", "Pleurozium schreberi", "Pohlia filum", "Pohlia wahlenbergii", 
    "Polytrichum juniperinum", "Polytrichum piliferum", "Ptilidium ciliare", "Sphagnum sp.", 
    "Sphagnum warnstorfii", "Stereocaulon sp.", "Stereocaulon capitatum", "Tomentypnum nitens"
]

tall_shrub_tundra_taxa = [
    # Tall Shrubs and stunted trees
    "Alnus viridis", "Betula exilis", "Betula fruticosa", "Betula glandulosa", "Betula nana",
    "Betula platyphylla", "Betula pubescens",
    "Larix cajanderi",  "Picea mariana", "Picea obovata", "Pinus pumila",
    "Salix alaxensis", "Salix glauca", "Salix pulchra", "Salix sp.",

    # Graminoids
    "Carex bigelowii","Carex lobularis", "Eriophorum vaginatum", "Juncus sp.",

    # Mosses, Lichens, and Liverworts
    "Aulacomnium turgidum", "Huperzia selago", "Hygrohypnum polare", "Hylocomium splendens", "Polytrichum hyperboreum", 
    "Sphagnum sp."
]


graminoid_dwarf_shrub_tundra_taxa = [
    # Dwarf shrubs
    "Andromeda polifolia","Arctostaphylos rubra", "Arctous alpina","Cassiope tetragona", "Dryas octopetala", "Diapensia lapponica", 
    "Empetrum hermaphroditum", "Empetrum nigrum", "Rhododendron lapponicum", "Rhododendron tomentosum", 
    "Salix sp.", "Salix arctica", "Salix reticulata", "Salix uva-ursi",
    "Vaccinium myrtillus", "Vaccinium uliginosum", "Vaccinium vitis-idaea",
    
    # Graminoids
    "Calamagrostis lapponica", "Carex aquatilis", "Carex bigelowii", "Carex stans", "Carex membranacea", "Carex rariflora", "Dupontia fischeri", 
    "Eriophorum angustifolium", "Eriophorum scheuchzeri", "Eriophorum sp.",
    "Eriophorum triste", "Eriophorum vaginatum", "Hierochloe pauciflora", "Luzula confusa", "Luzula nivea", "Phippsia algida", "Poaceae sp.",
    
    # Herbs and forbs
    "Campanula rotundifolia", "Cerastium alpinum", "Chamaenerion latifolium", "Euphrasia wettsteinii", "Polygonum viviparum", "Potentilla fruticosa", "Ranunculus hyperboreus", "Rumex arcticus",
    "Saxifraga paniculata",
    
    # Mosses, Lichens, and Liverworts
    "Allantoparmelia alpicola", "Andreaea blytti", "Andreaea rupestris", "Arctoparmelia incurva", "Aulacomnium turgidum", "Bryum cryophyllum", "Conostomum tetragonum",
    "Gymnomitrion corallioides", "Huperzia selago", "Hylocomium splendens", "Marsupella arctica", "Ochrolechia frigida", "Pleurocladula albescens", "Pogonatum fragile",
    "Polytrichum hyperboreum", "Polytrichum juniperinum", "Polytrichum piliferum","Psilopilum sp.", "Racomitrium lanuginosum", "Rhizocarpon cinereovirens", 
    "Rhizocarpon geographicum", "Rhizocarpon geminatum", "Sphagnum sp.", "Stereocaulon sp.", "Tomentypnum nitens",
]

aquatic_taxa = [
    # Algae
    "Chara sp.", "Caladophora sp.", "algae",
    
    # Aquatic macrophytes
    "Hippuris vulgaris", "Calliergon richardsonii",  
    "Ranunculus hyperboreus", "Eleocharis acicularis", 
    "Warnstorfia exannulata", "Scorpidium revolvens", "Potamogeton sp.", 
    "Potamogeton pectinatus", "Ruppia sp.", "Myriophillum spicatum", 
    "Sparaganium gramineum", "Sparaganium foliosum", "Persicaria amphibia", 
    "Potamogeton perfoliatus", "Nuphar lutea", "Sparganium emersum", 
    "Potamogeton natans", "Lobelia dortmanna", "Ceratophyllum demersum"
]

# Tricks to get everything to match the spreadsheet
cold_steppe_taxa = [t.strip() for t in cold_steppe_taxa]
forest_steppe_taxa = [t.strip() for t in forest_steppe_taxa]
boreal_forest_taxa = [t.strip() for t in boreal_forest_taxa]
tall_shrub_tundra_taxa = [t.strip() for t in tall_shrub_tundra_taxa]
graminoid_dwarf_shrub_tundra_taxa = [t.strip() for t in graminoid_dwarf_shrub_tundra_taxa]
aquatic_taxa = [t.strip() for t in aquatic_taxa]


# Function to check which taxa belong to a given biome
def check_biome(taxon_name, biome_list):
    if pd.isna(taxon_name):
        return 0
    # Strip whitespace to ensure exact matches
    clean_taxon = str(taxon_name).strip()
    return 1 if clean_taxon in biome_list else 0

# Apply the classification to create the biome ID matrix (stored as one biome per column in the spreadsheet)
df['Cold Steppe'] = df['Taxa'].apply(lambda x: check_biome(x, cold_steppe_taxa))
df['Forest-Steppe'] = df['Taxa'].apply(lambda x: check_biome(x, forest_steppe_taxa))
df['Boreal Forest'] = df['Taxa'].apply(lambda x: check_biome(x, boreal_forest_taxa))
df['Tall Shrub Tundra'] = df['Taxa'].apply(lambda x: check_biome(x, tall_shrub_tundra_taxa))
df['Graminoid Dwarf Shrub Tundra'] = df['Taxa'].apply(lambda x: check_biome(x, graminoid_dwarf_shrub_tundra_taxa))
df['Aquatic'] = df['Taxa'].apply(lambda x: check_biome(x, aquatic_taxa))

# Preview the results
print(df[['Taxa', 'Cold Steppe', 'Forest-Steppe', 'Boreal Forest', "Tall Shrub Tundra", 'Graminoid Dwarf Shrub Tundra', 'Aquatic']].head())

# Export to a new Excel file. This is the file that the proxy model code uses.
df.to_excel("species_summary_stats_with_biomes.xlsx", index=False)
print("Classification complete! Exported to 'species_summary_stats_with_biomes.xlsx'")