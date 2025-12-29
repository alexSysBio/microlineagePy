"""
author Alexandros Papagiannakis, HHMI @Stanford University, 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
import lineator as linpy

def select_points_from_plot(df_to_plot, x_col='frame', y_col='y', z_col='cell_trajectory_id'):
    trajectory_ids = []
    selected_indices = []
    df = df_to_plot.reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(df[x_col], df[y_col], picker=5)
    ax.set_title("1/3: Click points to select. Press 'Enter' to compute lineage.", fontsize=14)
    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)
    ax.grid(True)
    
    def on_pick(event):
        index = event.ind[0]
        if index not in selected_indices:
            print(f"  Selected Point -> Index: {index}, Coords: ({df[x_col].iloc[index]:.2f}, {df[y_col].iloc[index]:.2f}), ID: {df[z_col].iloc[index]}")
            selected_indices.append(index)
            trajectory_ids.append(df[z_col].iloc[index])
            ax.scatter(df[x_col].iloc[index], df[y_col].iloc[index], 
                       facecolors='none', edgecolors='red', s=100, linewidths=1.5)
            fig.canvas.draw_idle()

    def on_key(event):
        if event.key == 'enter':
            plt.close(fig)

    fig.canvas.mpl_connect('pick_event', on_pick)
    fig.canvas.mpl_connect('key_press_event', on_key)
    
    while plt.fignum_exists(fig.number):
        plt.pause(0.1)
        
    return trajectory_ids

# ----------------------------------------------------#
#  MODIFIED Main Script Logic with TERMINAL CONFIRMATION #
# ----------------------------------------------------#
def select_lineages(linked_df):
    all_lineage_data = {}

    for exp in linked_df.experiment.unique():
        exp_df = linked_df[linked_df.experiment == exp]
        
        # --- NEW: Convert `for pos` loop to a `while` loop for manual control ---
        positions = exp_df.position_int.unique()
        pos_index = 0
        while pos_index < len(positions):
            pos = positions[pos_index]
            pos_df = exp_df[exp_df.position_int==pos]
            reselect_current_position = True
            while reselect_current_position:
                print(f"\n--- Launching selection for Exp: {exp}, Pos: {pos} ---")
                
                trajectory_ids = select_points_from_plot(pos_df, z_col='cell_trajectory_id')
                
                if not trajectory_ids:
                    print("  > No points selected for this position.")
                    # Break the inner re-select loop and proceed to the terminal confirmation
                    break

                mother_trajectories = np.unique(trajectory_ids)
                final_mother_lineages = []
                final_sister_dict = {}
                for traj in mother_trajectories:
                    lineage_list, new_sisters = linpy.compute_lineage([traj], {}, pos_df)
                    final_mother_lineages.extend(lineage_list)
                    final_sister_dict.update(new_sisters)
                
                final_mother_lineages = list(set(final_mother_lineages))

                fig, ax = plt.subplots(figsize=(10, 7))
                sister_values = [v for v in final_sister_dict.values() if pd.notna(v)]
                lineage_ids = final_mother_lineages + sister_values
                other_df = pos_df[~pos_df.cell_trajectory_id.isin(lineage_ids)]
                ax.scatter(other_df.frame, other_df.y, c='lightgray', s=20, alpha=0.7, label='Other Cells')
                aged_df = pos_df[pos_df.cell_trajectory_id.isin(final_mother_lineages)]
                ax.scatter(aged_df.frame, aged_df.y, c='#ff7f0e', label='Aging Lineage')
                yng_df = pos_df[pos_df.cell_trajectory_id.isin(sister_values)]
                ax.scatter(yng_df.frame, yng_df.y, c='#2ca02c', label='Sister Lineage')
                ax.set_xlabel('Frames', fontsize=14)
                ax.set_ylabel('Y coordinates', fontsize=14)
                ax.set_title(f"Result for Exp: {exp}, Pos: {pos}\n2/3: Press 'Enter' to ACCEPT, 'r' to RE-SELECT", fontsize=14)
                ax.legend()
                ax.grid(True)
                
                user_choice_holder = ['accept']
                def handle_confirmation(event):
                    if event.key == 'enter':
                        user_choice_holder[0] = 'accept'
                        plt.close(event.canvas.figure)
                    elif event.key == 'r':
                        user_choice_holder[0] = 'reselect'
                        plt.close(event.canvas.figure)
                
                fig.canvas.mpl_connect('key_press_event', handle_confirmation)
                
                while plt.fignum_exists(fig.number):
                    plt.pause(0.1)
                
                if user_choice_holder[0] == 'reselect':
                    print("  > Re-selecting for the same position...")
                else: 
                    print("  > Selection accepted.")
                    if trajectory_ids: # Only store if something was actually selected
                        result_key = (exp, pos)
                        all_lineage_data[result_key] = {
                            'aged_lineage_ids': final_mother_lineages,
                            'sister_map': final_sister_dict
                        }
                        print(f"  > Stored lineage data for ({exp}, {pos}).")
                    reselect_current_position = False

            # --- NEW: Terminal confirmation step ---
            advance_to_next = False
            while not advance_to_next:
                user_input = input("3/3: Move to next position? (yes/no): ").lower().strip()
                if user_input in ['yes', 'y']:
                    pos_index += 1  # This advances the main `while` loop
                    advance_to_next = True
                elif user_input in ['no', 'n']:
                    print("Repeating selection for the current position.\n")
                    advance_to_next = True # Exit this input loop, but pos_index is not incremented
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

    return all_lineage_data


def save_lineage_data(all_lineage_data, save_path):
    with open(save_path+'/all_lineages_data', 'wb') as handle:
        pickle.dump(all_lineage_data, handle)
    


