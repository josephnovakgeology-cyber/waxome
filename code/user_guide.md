# User Guide
## Getting Started
### Thanks for checking out Waxome! 
We really appreciate you checking out our work. This document is meant to help you get started by showing you how to set up the required python environment and walking you through reproducing the analysis of the n-alkane data with Waxome over the last 250 Ka in a sediment core composite section from Lake Baikal's Academician Ridge. This user guide is intended for folks who are unfamiliar with python. 

If you are looking for information on how to update Waxome with new data or on how to adapt it to a different environment, please check out instructions.md in the "how_to_update_model" folder. 

### Setting up the python environment
Waxome has several dependencies that you will need to install into a python environment for you to get up and running. For convenience, I made a .yml file that you can use to do that. For the guide, I assume that you are using Spyder and conda, since that is the only way I know how to do this. 

To get started, open Anaconda prompt (PC) or the terminal (Mac). You should see something like this:
<img width="200" height="35" alt="image" src="https://github.com/user-attachments/assets/8be845bf-d572-4bda-994a-1dfbf28cad5e" />

You need to use the "cd" terminal command to navigate to where the .yml file is on your computer. For me, that command looks like this:
cd C:\Users\josep\OneDrive\Documents\papers\alkane_biomization\code\github_version

Once you've done that, type in this command to set up the environment:
conda env create -f waxome_env.yml

It will look like you are hacking into the mainframe for a minute or two. 

Once that is done, your environment is set up and ready to roll. 
## Analyzing sedimentary n-alkane distributions with Waxome
### Disclaimer
The version of Waxome presented here is intended for application from Northern Hemisphere boreal environments (i.e., the Arctic and sub-Arctic). This model is not appropriate to use elsewhere because the vegetation data that parameterizes the model and the biomes it describes are particular to the Arctic and sub-Arctic. 

Waxome also assumes that you are analyzing thermally immature n-alkanes. Check out the CPI of your samples to make sure it is a reasonable value for this purpose. 

Make sure you are using the tool appropriately. 

### Preparing your data
Download the scripts and supporting .xlsx files from Github. In the same folder where you found the user guide, there is a file called "baikal_250ka_alkanes.xlsx"
This file is intended to be the data for this demo in addition to the template for how you will need to format your n-alkane data to use the model. The important
headers are fC23, fC25, etc. - these are the fractional abundances of the C23-C31, odd n-alkanes. These values must sum to 1. Do not include other n-alkane chain lengths, it will mess up the model because the modern plant data only include C23-C31, odd.

If you want to add more chain lengths, you will need to re-parameterize the model. Instructions and supporting code for how to do that are in "how_to_update_model" folder.

### Running the script
To run Waxome, open the run_waxome.py file (no kidding). run_waxome.py needs to be in the same folder as waxome.py for the code to work. Personally, I prefer to also keep the species_summary_stats_with_biomes.xlsx and your baikal_250ka_alkanes.xlsx files in the same folder also.

The code should look like this:

<img width="1031" height="747" alt="image" src="https://github.com/user-attachments/assets/c3a9abb2-4ac1-422a-b1c7-b01ede020e65" />

**If you are not super familiar with python, it is important to understand that your python interpreter must be directed towards the waxome_env python environment we made for the code to work. In Spyder (which is what I know how to use), you can change that by clicking "tools" on the top ribbon, then "preferences", then "python interpreter." Then change the python interpreter to be the waxome_env environment and restart the kernel. You also need to set Spyder's working directory to be the folder where the waxome.py and run_waxome.py (and probably the .xlsx files containing species_data sediment_data unless you want to use a long file path name) are co-located. You will want to change the python interpreter setting when you are done using Waxome so that you do not forget that it is set as the default active environment the next time you use spyder.**

To run your data or the demo, you need to update the file paths for species_data (line 29 of the code) and sediment_data (L30). I purposely included two different versions of how that can be done as examples. You can either call the entire directory path (formatted for my PC on L29), or you can search within your current folder (formatted as in L30). 

The other variables you should update is the study_site on L46, unless you are running the demo dataset from Lake Baikal, and the number of NMF endmembers.
The number of endmember can be hard to know before you start exploring your data, so you will likely want to run Waxome more than once (see the Scree plot below).

After that, run the script, which in Spyder is done by pressing the little green arrow on the top ribbon here:

<img width="1917" height="1130" alt="image" src="https://github.com/user-attachments/assets/0179743a-4efd-4d8e-a80b-e7780f53aa33" />

When the script is running, you will see this in the console:
<img width="950" height="587" alt="image" src="https://github.com/user-attachments/assets/fca4d30d-f68a-45e9-ba74-8182c555c7e8" />

When it finishes, you will see a printout like this:
<img width="845" height="732" alt="image" src="https://github.com/user-attachments/assets/cb870c3a-89c5-4623-96f1-7fdcc0a2e29c" />

The way to interpret this printout is that the most likely biomes represented by endmember 1 are graminoid (cold steppe and graminoid dwarf shrub tundra), and that the most likely biome represented by endmember 2 is woody (boreal forest).

Looking at the plots, the first important one is the Scree plot, pasted below:

<img width="1065" height="633" alt="image" src="https://github.com/user-attachments/assets/c9c2b27e-3937-4e7f-8ac1-76f526f8b582" />

This plot helps give a sense of the appropriate number of NMF endmembers for your site. The way to interpret it is that the inflection point or 'elbow' is the appropriate number to stop at. Here, that number is 2 endmembers. 

<img width="1413" height="993" alt="image" src="https://github.com/user-attachments/assets/4ab0ef1d-4233-43d6-a918-e08c715753e3" />

The next plot is the PCA plot, which shows a projection of the sediment samples onto the PCA space of the Waxome simulations. There are a couple of things to look for here. Firstly, do your sediment samples (white stars) fall within the cloud of colored points (the Waxome simulations?). Secondly, do the endmembers (white Xs) plot in a region that makes sense for the identified most likely endmember based on the printout in the console? 

The last plot to help you think about your endmember identities is the barplot pasted below:

<img width="853" height="619" alt="image" src="https://github.com/user-attachments/assets/84a3fd82-26ac-47b5-be58-10502f103121" />

You can compare the shape of these barplots to those of the biome centroids in the Waxome manuscript. The assigned identities should look qualitatively similar to what you see for the centroid value of that biome. 

