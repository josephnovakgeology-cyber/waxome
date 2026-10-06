# Instructions
## So, you want to update Waxome, huh?
Bold. I'll try to help you with these brief instructions.

## Updating Waxome by adding more observations of the same species in the database.
This is by far the easiest thing that can be done. To do it, you just need to add more rows in the plant_data.xlsx spreadsheet. Make sure that any text is typed in exactly the same way (including spaces, capitalization, etc.) as the taxa names already in the sheet. 

From there, just run the two scripts in this folder in the following order:
  1). calculate_species_means.py
  2). assign_species_to_biomes.py

These two scripts collectively build the species_summary_stats_with_biomes.xlsx spreadsheet that waxome.py needs to run.

## Updating Waxome by adding new taxa. 
This is slightly harder. You need to determine which biome or biomes this new taxon belongs to. From there, the name should be added to the species lists in assign_species_to_biomes.py. You then run the two files in the order specified above. 
