"""
Phase 4: Feature Extraction
Lead: K. B. Sohith Chowdary (BL.SC.U4AIE24124)
"""

import pandas as pd
import numpy as np

def extract_features(input_file, output_file='outputs/extracted_features.tsv'):
    """Extract statistical features from gene expression data"""
    
    print("=" * 70)
    print("PHASE 4: FEATURE EXTRACTION")
    print("=" * 70)
    
    # Load data
    print("\n[1] Loading selected genes...")
    df = pd.read_csv(input_file, sep='\t')
    print(f"    Loaded: {df.shape[0]} genes × {df.shape[1]} columns")
    
    # Extract expression matrix
    print("\n[2] Extracting features...")
    expr_matrix = df.iloc[:, 1:].values
    gene_ids = df['Gene'].values
    
    # Create feature dataframe
    features = pd.DataFrame()
    features['Gene'] = gene_ids
    
    # Statistical features
    features['Mean_Expression'] = np.mean(expr_matrix, axis=1)
    features['Std_Expression'] = np.std(expr_matrix, axis=1)
    features['Median_Expression'] = np.median(expr_matrix, axis=1)
    features['Max_Expression'] = np.max(expr_matrix, axis=1)
    features['Min_Expression'] = np.min(expr_matrix, axis=1)
    features['CV_Expression'] = (features['Std_Expression'] / 
                                (features['Mean_Expression'] + 1e-5))
    
    print(f"    Features extracted: {features.shape[1] - 1}")
    print(f"    Total genes: {features.shape[0]}")
    
    # Feature statistics
    print("\n[3] Feature Statistics:")
    print(f"    Mean Expression: {features['Mean_Expression'].mean():.2f} ± {features['Mean_Expression'].std():.2f}")
    print(f"    Std Expression: {features['Std_Expression'].mean():.2f} ± {features['Std_Expression'].std():.2f}")
    
    # Save features
    print(f"\n[4] Saving features...")
    features.to_csv(output_file, sep='\t', index=False)
    print(f"    Saved to: {output_file}")
    
    print("\n" + "=" * 70)
    print("✓ PHASE 4 COMPLETE")
    print("=" * 70 + "\n")
    
    return features

if __name__ == "__main__":
    extract_features('outputs/selected_similar_genes.tsv')
