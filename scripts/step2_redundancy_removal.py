"""
Phase 2: Redundancy Removal
Lead: B. Deva Harsha (BL.SC.U4AIE24111)
"""

import pandas as pd
import numpy as np

def remove_redundancy(input_file, output_file='outputs/non_redundant_data.tsv', 
                      threshold=0.95):
    """Remove redundant genes based on correlation"""
    
    print("=" * 70)
    print("PHASE 2: REDUNDANCY REMOVAL")
    print("=" * 70)
    
    # Load data
    print("\n[1] Loading curated data...")
    df = pd.read_csv(input_file, sep='\t')
    print(f"    Loaded: {df.shape[0]} genes × {df.shape[1]} columns")
    
    # Extract expression matrix
    print("\n[2] Extracting expression matrix...")
    expr_matrix = df.iloc[:, 1:].values
    gene_ids = df['Gene'].values
    print(f"    Expression matrix: {expr_matrix.shape}")
    
    # Compute correlation matrix
    print(f"\n[3] Computing Pearson correlation matrix...")
    corr_matrix = np.corrcoef(expr_matrix)
    print(f"    Correlation matrix computed: {corr_matrix.shape}")
    
    # Find redundant genes
    print(f"\n[4] Identifying redundant genes (r > {threshold})...")
    to_remove = set()
    for i in range(len(gene_ids)):
        for j in range(i+1, len(gene_ids)):
            if corr_matrix[i, j] > threshold and i not in to_remove:
                to_remove.add(j)
    
    print(f"    Redundant genes to remove: {len(to_remove)}")
    
    # Remove redundant genes
    print(f"\n[5] Removing redundant genes...")
    non_redundant_indices = [i for i in range(len(gene_ids)) 
                            if i not in to_remove]
    df_non_redundant = df.iloc[non_redundant_indices].reset_index(drop=True)
    
    # Save non-redundant data
    print(f"\n[6] Saving non-redundant dataset...")
    df_non_redundant.to_csv(output_file, sep='\t', index=False)
    print(f"    Saved to: {output_file}")
    
    print("\n" + "=" * 70)
    print("✓ PHASE 2 COMPLETE")
    print("=" * 70 + "\n")
    
    return df_non_redundant

if __name__ == "__main__":
    remove_redundancy('outputs/curated_data.tsv')
