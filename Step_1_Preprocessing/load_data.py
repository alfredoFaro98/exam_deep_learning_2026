import pandas as pd
import numpy as np
import os

def load_and_process_data(data_dir):
    print("Loading data from:", data_dir)
    
    # 1. Load Coordinates
    coord_path = os.path.join(data_dir, 'coordinates.csv')
    if os.path.exists(coord_path):
        print("Loading coordinates...")
        # Based on notebook: sep=';'
        coords_df = pd.read_csv(coord_path, header=None, index_col=False, sep=';')
        
        # Drop timestamp (column 0)
        coords_data = coords_df.iloc[:, 1:].values
        print(f"Coordinates shape after dropping timestamp: {coords_data.shape}") # Should be (50001, 414)
    else:
        print("coordinates.csv not found.")
        coords_data = None

    # 2. Load Forces
    forces_path = os.path.join(data_dir, 'forces.csv')
    if os.path.exists(forces_path):
        print("Loading forces...")
        # Based on notebook: seems to require splitting by tab or whitespace
        # Try reading with sep='\t' first
        try:
            forces_df = pd.read_csv(forces_path, header=None, sep='\t')
            if forces_df.shape[1] == 1:
                 # Fallback if it didn't parse correctly
                 forces_df = pd.read_csv(forces_path, header=None, sep='\s+', engine='python')
        except:
             forces_df = pd.read_csv(forces_path, header=None, sep=None, engine='python')

        # Check if we need to split manually like in the notebook
        if forces_df.shape[1] == 1:
             print("Manual split required for forces...")
             forces_df = forces_df[0].str.split('\t', expand=True)
             forces_df = forces_df.apply(pd.to_numeric, errors='coerce')
        
        # Drop timestamp (column 0)
        forces_data = forces_df.iloc[:, 1:].values
        print(f"Forces shape after dropping timestamp: {forces_data.shape}")
    else:
        print("forces.csv not found.")
        forces_data = None

    # 3. Load Velocities
    velocity_path = os.path.join(data_dir, 'velocity.csv')
    if os.path.exists(velocity_path):
        print("Loading velocities...")
        # Similar logic to forces
        try:
            velocity_df = pd.read_csv(velocity_path, header=None, sep='\t')
            if velocity_df.shape[1] == 1:
                velocity_df = pd.read_csv(velocity_path, header=None, sep='\s+', engine='python')
        except:
            velocity_df = pd.read_csv(velocity_path, header=None, sep=None, engine='python')
            
        if velocity_df.shape[1] == 1:
             print("Manual split required for velocities...")
             velocity_df = velocity_df[0].str.split('\t', expand=True)
             velocity_df = velocity_df.apply(pd.to_numeric, errors='coerce')

        # Drop timestamp (column 0)
        velocity_data = velocity_df.iloc[:, 1:].values
        print(f"Velocities shape after dropping timestamp: {velocity_data.shape}")
    else:
        print("velocity.csv not found.")
        velocity_data = None
        
    return coords_data, forces_data, velocity_data

if __name__ == "__main__":
    data_dir = r"c:\Users\alfredo\Desktop\Protein Dynamics"
    coords, forces, vels = load_and_process_data(data_dir)
    
    # Reshape to (Time, Atoms, 3) 
    # 414 columns = 138 atoms * 3 coords (x,y,z)
    n_atoms = 138
    target_cols = n_atoms * 3
    
    if coords is not None:
        print(f"Coords raw shape: {coords.shape}")
        if coords.shape[1] == target_cols:
            coords_reshaped = coords.reshape(-1, n_atoms, 3)
            print(f"Reshaped Coordinates: {coords_reshaped.shape}")
        else:
            print(f"Coords shape mismatch. Expected {target_cols}, got {coords.shape[1]}")
        
    if forces is not None:
        print(f"Forces raw shape: {forces.shape}")
        if forces.shape[1] > target_cols:
             print(f"Forces has extra columns ({forces.shape[1]}), slicing to first {target_cols}...")
             forces = forces[:, :target_cols]
        
        if forces.shape[1] == target_cols:
            forces_reshaped = forces.reshape(-1, n_atoms, 3)
            print(f"Reshaped Forces: {forces_reshaped.shape}")
        else:
             print(f"Forces shape mismatch. Expected {target_cols}, got {forces.shape[1]}")
        
    if vels is not None:
        print(f"Vels raw shape: {vels.shape}")
        if vels.shape[1] > target_cols:
             print(f"Vels has extra columns ({vels.shape[1]}), slicing to first {target_cols}...")
             vels = vels[:, :target_cols]

        if vels.shape[1] == target_cols:
            vels_reshaped = vels.reshape(-1, n_atoms, 3)
            print(f"Reshaped Velocities: {vels_reshaped.shape}")
        else:
             print(f"Vels shape mismatch. Expected {target_cols}, got {vels.shape[1]}")
