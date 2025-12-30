# 🔬 microlineagePy 🔀
This repository contains a set of functions that can be used to link cells into lineages. 

The <code>compute_lineage</code> function inside the <code>lineator.py</code> script is used to link mother and daughter cells into lineages, starting from the older progeny, towards the youngest mother. This function is applied on a dataframe that follows the lineage nomenclature implemented in my publicly available data: <url>https://www.ebi.ac.uk/biostudies/BioImages/studies/S-BIAD1658?query=papagiannakis</url>: 
<ul> <code>"experiment": a unique experiment ID which includes the field of view (i.e., "xy01") and the date of the experiment </code></ul>
<ul> <code>"position_int": integer values that corespond to the microfluidics channel number within each field of view and experiment </code></ul>
<ul> <code>"cell_trajectory_id": the unique ID of the cell cycle </code></ul>
<ul> <code>"mother_cell": the unique ID of the predivisional mother cell for each cell cycle </code></ul> 
<ul> <code>"frame": the frame number into the timelapse experiment </code></ul> 
<ul> <code>"y": the y-coordinates of the cells along the microfluidics channel </code></ul>

