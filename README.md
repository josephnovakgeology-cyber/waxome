# waxome
A series of python scripts for running the Waxome n-alkane forward proxy model. The user guide is in the code folder.

This version of the model is parameterized to reconstruct vegetation change through time from n-alkanes in boreal Northern Hemisphere environments. 

Waxome is based upon the hypothesis that the aggregate n-alkane signal of the vegetation on a landscape arises from the interaction of three processes: (1) the plant taxa within the vegetation assemblage, (2) the relative abundances of the plant functional types which those taxa represent, and (3) the rates at which different plant taxa produce plant waxes. Waxome uses a database of individual plant n-alkane measurements, parameterized plant functional type abundances, and biome-taxon assignments to simulate the possible n-alkane distributions produced by different biomes. These distributions are then used to identify the likely sources of the n-alkane endmembers contributing to plant wax profiles in sediment samples, which are derived independently from Waxome by non-negative matrix factorization of the sedimentary n-alkane profiles (Lee & Seung, 1999; Polissar et al., 2025). The version of the model archived here is parameterized with n-alkane data from 548 individual terrestrial plants, aquatic macrophytes, and algae belonging to 171 taxa. These data were compiled from the literature and the associated references can be found in the manuscript. 

The manuscript describing Waxome is currently in review. Use this code at your own risk. If you are reviewing the manuscript and there are issues setting up the python environment, please contact me directly at: joseph_novak@brown.edu. I am happy to help, and I will incorporate the solutions to your problem into the code's user guide documentation. My goal is to make this easily usable for anyone who is interested, but I am new at this so I am bound to make mistakes setting things up for reuse.

Wax on, wax off. 

References:

Lee, D. D., & Seung, H. S. (1999). Learning the parts of objects by non-negative matrix factorization. Nature, 401(6755), 788–791. https://doi.org/10.1038/44565

Polissar, P. J., Karp, A. T., & D’Andrea, W. J. (2025). Mixed messages: Unmixing sedimentary molecular distributions reveals source contributions and isotopic values. Geochimica et Cosmochimica Acta, 396, 122–134. https://doi.org/10.1016/j.gca.2025.03.001
