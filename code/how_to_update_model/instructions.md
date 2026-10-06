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

## Re-parameterizing Waxome for new environments (making new biomes).
This is super tough, because it will require you to completely redo the a major part of putting together Waxome - the literature review and database compilation.
So, if you did that already, you will have a reasonable idea of the general biomes in your region of interest and you should have a massive spreadsheet with a bunch of plant taxa names. You should also know which biomes or biomes each taxon belongs to.

For the scripts to work, you should use the plant_data.xlsx sheet in this folder as a template. The Waxome code and helper scripts were written to be flexible with the number of n-alkane chain lengths in the supporting .xlsx files (I did not test that, but it should be the case because the n-alkane chain lengths are not hard-coded). So, set the spreadsheet up to include as many n-alkane chain lengths as you want (you can also include the evens). Once that is formatted, the code will need to be changed in the following places:

in assign_species_to_biomes.py, you will need to update the biome lists, shown in part here:

<img width="1048" height="933" alt="image" src="https://github.com/user-attachments/assets/d2aac3b8-e186-45a6-b2a3-cf867c59d69e" />

You will also need to update the IDs in the code that creates the biome ID matrix, shown here:
<img width="972" height="483" alt="image" src="https://github.com/user-attachments/assets/dd9d66a7-2584-44fd-ae44-cf582028944e" />

The other big task will be updating the load_waxome_parameterization function in waxome.py, shown here:
<img width="998" height="867" alt="image" src="https://github.com/user-attachments/assets/bebec653-c3f0-4f0c-bc0a-30411e5e3479" />

The tricky part about this step is that you need to estimate the PFT abundance bounds in the biome_bounds matrix. This will require an extensive literature review.

