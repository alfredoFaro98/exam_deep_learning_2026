import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import joblib
import os
from load_data import load_and_process_data

def preprocess_and_analyze(data_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Load Data
    coords, forces, vels = load_and_process_data(data_dir)
    if coords is None:
        raise ValueError("Could not load coordinates.")

    print(f"Original Coords Shape: {coords.shape}") # (50001, 138, 3)

    # 2. Reshape for Analysis (Time, Features)
    # Features = Atoms * 3
    # Note: load_and_process_data returns (50001, 138, 3) ONLY if reshaping works, but here it returns (50001, 414) in some cases.
    # Actually, load_and_process_data returns raw numpy arrays BEFORE reshaping in the main block.
    # But wait, looking at load_data.py, it returns raw (n_samples, n_features).
    
    # Check shape
    if len(coords.shape) == 3:
         n_timesteps, n_atoms, n_dims = coords.shape
         coords_flat = coords.reshape(n_timesteps, -1)
    else:
         n_timesteps, n_features = coords.shape
         coords_flat = coords
    
    print(f"Flattened Coords Shape: {coords_flat.shape}")

    # 3. Standardization
    # Deep Learning models converge faster with standardized data
    print("Standardizing data...")
    scaler = StandardScaler()
    coords_scaled = scaler.fit_transform(coords_flat)
    
    # Save scaler for later inverse transform
    joblib.dump(scaler, os.path.join(output_dir, 'scaler.pkl'))

    # 4. Dimensionality Reduction (PCA)
    # We want to capture e.g. 95% of variance or use a fixed number of components
    print("Running PCA...")
    pca = PCA(n_components=0.95) # Keep 95% variance
    coords_pca = pca.fit_transform(coords_scaled)
    
    print(f"PCA Reduced Shape: {coords_pca.shape}")
    print(f"Number of components to explain 95% variance: {pca.n_components_}")

    # Save PCA model
    joblib.dump(pca, os.path.join(output_dir, 'pca_model.pkl'))
    
    # Save Processed Data
    np.save(os.path.join(output_dir, 'coords_pca.npy'), coords_pca)

    # 5. Analysis Plots
    # Explained Variance Ratio
    plt.figure(figsize=(10, 6))
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.title('PCA Explained Variance Analysis')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'pca_variance_plot.png'))
    plt.close()

    # Plot first 2 PCs (Trajectory in latent space) if possible
    if coords_pca.shape[1] >= 2:
        plt.figure(figsize=(10, 6))
        plt.scatter(coords_pca[:, 0], coords_pca[:, 1], alpha=0.1, s=1, c=np.arange(n_timesteps), cmap='viridis')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.title('Protein Trajectory in PC Space')
        plt.colorbar(label='Timestep')
        plt.savefig(os.path.join(output_dir, 'trajectory_pca_plot.png'))
        plt.close()
    else:
        # Plot single PC over time
        plt.figure(figsize=(10, 6))
        plt.plot(coords_pca[:, 0], label='PC1')
        plt.xlabel('Timestep')
        plt.ylabel('PC1 Value')
        plt.title('Protein Trajectory (PC1)')
        plt.legend()
        plt.savefig(os.path.join(output_dir, 'trajectory_pca_plot.png'))
        plt.close()
    
    return coords_pca

if __name__ == "__main__":
    data_dir = r"c:\Users\alfredo\Desktop\Protein Dynamics"
    output_dir = r"c:\Users\alfredo\Desktop\Protein Dynamics\processed_data"
    
    try:
        data_pca = preprocess_and_analyze(data_dir, output_dir)
        print("Preprocessing and Analysis Complete.")
    except Exception as e:
        print(f"Error: {e}")
