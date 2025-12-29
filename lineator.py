# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 15:43:45 2025

@author: Alexandros Papagiannakis, HHMI @Stanford University, 2025
"""

import pandas as pd
import numpy as np

class NoMotherCellError(Exception):
    pass
class NoSisterCellError(Exception):
    pass

def get_mother_cell(cell_trajectory, cell_dataframe):
    mother_cell = cell_dataframe[cell_dataframe.cell_trajectory_id == cell_trajectory].mother_cell.values[0]
    return mother_cell

def get_mother_trajectory(cell_trajectory, cell_dataframe):
    mother_cell = get_mother_cell(cell_trajectory, cell_dataframe)
    if pd.notna(mother_cell) and mother_cell in cell_dataframe.cell_id.unique():
        return cell_dataframe[cell_dataframe.cell_id == mother_cell].cell_trajectory_id.values[0]
    else:
        raise NoMotherCellError(f'This cell trajectory {cell_trajectory} is not linked to a mother cell.')

def get_sister_trajectory(cell_trajectory, mother_trajectory, cell_dataframe):
    mother_cell = get_mother_cell(cell_trajectory, cell_dataframe)
    sister_trajectories = cell_dataframe[cell_dataframe.mother_cell == mother_cell].cell_trajectory_id.unique().tolist()
    sister_trajectories = np.array(sister_trajectories)
    if sister_trajectories.shape[0] == 2:
        return sister_trajectories[sister_trajectories != cell_trajectory][0]
    else:
        raise NoSisterCellError(f'This cell trajectory {cell_trajectory} does not share a mother cell with another trajectory.')

def compute_lineage(cell_trajectory_list, sister_dictionary, cell_dataframe):
    try:
        mother_trajectory = get_mother_trajectory(cell_trajectory_list[-1], cell_dataframe)
    except (NoMotherCellError, RecursionError):
        return cell_trajectory_list, sister_dictionary
    try:    
        sister_trajectory = get_sister_trajectory(cell_trajectory_list[-1], mother_trajectory, cell_dataframe)
        sister_dictionary[cell_trajectory_list[-1]] = sister_trajectory
    except NoSisterCellError:
        sister_dictionary[cell_trajectory_list[-1]] = np.nan
    cell_trajectory_list.append(mother_trajectory)
    return compute_lineage(cell_trajectory_list, sister_dictionary, cell_dataframe)