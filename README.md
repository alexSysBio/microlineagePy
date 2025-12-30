# 🔬 microlineagePy 🔀
This repository contains a set of functions that can be used to link cells into lineages. 

The <code>compute_lineage</code> function inside the <code>lineator.py</code> script is used to link mother and daughter cells into lineages, starting from the older progeny, towards the youngest mother. This function is applied on a dataframe that follows the lineage nomenclature implemented in my publicly available data: <url>https://www.ebi.ac.uk/biostudies/BioImages/studies/S-BIAD1658?query=papagiannakis</url>: 
<ul> <code>"experiment": a unique experiment ID which includes the field of view (i.e., "xy01") and the date of the experiment </code></ul>
<ul> <code>"position_int": integer values that corespond to the microfluidics channel number within each field of view and experiment </code></ul>
<ul> <code>"cell_trajectory_id": the unique ID of the cell cycle </code></ul>
<ul> <code>"mother_cell": the unique ID of the predivisional mother cell for each cell cycle </code></ul> 
<ul> <code>"frame": the frame number into the timelapse experiment </code></ul> 
<ul> <code>"y": the y-coordinates of the cells along the microfluidics channel </code></ul>

This nomenclature can party be adjusted in the <code> select_points_from_plot(df_to_plot, x_col='frame', y_col='y', z_col='cell_trajectory_id') </code> function in the <code> lineage_selector.py </code> script.

The <compute_lineage> function is implemented in the <code> lineage_selector.py </code> script which opens a graphic interface to select sell lineages for each microfluidics channel (<code>"position_int"</code>), field of view and experiment (<code>"experiment"</code>: contains both the date and the xy position). The lineage is drawn backwards, from past to present. The result is a list, which contains all cell trajectory IDs in the lineage, and a dictionary which matches the cell_trajectory_id of each mother cell, with that of its sister. 

![Alt text](https://github.com/alexSysBio/microlineagePy/blob/main/lineage_figure_5.png)
