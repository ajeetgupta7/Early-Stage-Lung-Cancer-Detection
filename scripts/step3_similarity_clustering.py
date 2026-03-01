"""
Phase 3: Similarity-Based Clustering
Lead: Mamidi Yeswanth (BL.SC.U4AIE24131)
"""

import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
import matplotlib.pyplot as plt

def cluster_genes(input_file, output_file='outputs/selected_similar_genes.tsv',
                  distance_threshold=0.4):
    """Perform hierarchical clustering on gene expression data"""
    
    print("=" * 70)
    print("PHASE 3: SIMILARITY-BASED CLUSTERING")
    print("=" * 70)
    
    # Load data
    print("\n[1] Loading non-redundant data...")
    df = pd.read_csv(input_file, sep='\t')
    print(f"    Loaded: {df.shape[0]} genes × {df.shape[1]} columns")
    
    # Extract expression matrix
    print("\n[2] Preparing data for clustering...")
    expr_matrix = df.iloc[:, 1:].values
    gene_ids = df['Gene'].values
    
    # Perform hierarchical clustering
    print(f"\n[3] Performing hierarchical clustering...")
    Z = linkage(expr_matrix, method='average', metric='correlation')
    print(f"    Clustering complete")
    
    # Apply distance threshold
    print(f"\n[4] Applying distance threshold ({distance_threshold})...")
    clusters = fcluster(Z, t=distance_threshold, criterion='distance')
    n_clusters = len(set(clusters))
    print(f"    Number of clusters: {n_clusters}")
    
    # Select representatives
    print(f"\n[5] Selecting cluster representatives...")
    selected_indices = []
    for cluster_id in sorted(set(clusters)):
        cluster_genes_idx = np.where(clusters == cluster_id)[0]
        selected_indices.append(cluster_genes_idx[0])
    
    df_selected = df.iloc[selected_indices].reset_index(drop=True)
    print(f"    Selected genes: {len(df_selected)}")
    
    # Save selected genes
    print(f"\n[6] Saving selected genes...")
    df_selected.to_csv(output_file, sep='\t', index=False)
    print(f"    Saved to: {output_file}")
    
    # Create dendrogram
    print(f"\n[7] Creating dendrogram visualization...")
    plt.figure(figsize=(14, 6))
    dendrogram(Z, truncate_mode='lastp', p=30)
    plt.title('Gene Expression Hierarchical Clustering Dendrogram')
    plt.xlabel('Cluster Index')
    plt.ylabel('Distance (1 - correlation)')
    plt.tight_layout()
    plt.savefig('outputs/clustering_dendrogram.png', dpi=150)
    print(f"    Dendrogram saved")
    
    print("\n" + "=" * 70)
    print("✓ PHASE 3 COMPLETE")
    print("=" * 70 + "\n")
    
    return df_selected

if __name__ == "__main__":
    cluster_genes('outputs/non_redundant_data.tsv')
