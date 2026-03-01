"""
Phase 1: Data Curation
Lead: Ajeet Gupta (BL.SC.U4AIE24167)
"""

import pandas as pd
import numpy as np

def curate_data(input_file, output_file='outputs/curated_data.tsv'):
    """Perform data curation on gene expression dataset"""
    
    print("=" * 70)
    print("PHASE 1: DATA CURATION")
    print("=" * 70)
    
    # Load data
    print("\n[1] Loading dataset...")
    df = pd.read_csv(input_file, sep='\t')
    original_shape = df.shape
    print(f"    Original shape: {original_shape[0]} genes × {original_shape[1]} columns")
    
    # Check for NaN values
    print("\n[2] Handling missing values...")
    missing_count = df.isnull().sum().sum()
    print(f"    Total NaN values found: {missing_count}")
    
    if missing_count > 0:
        df = df.dropna()
        print(f"    After removing NaN: {df.shape[0]} genes")
    else:
        print(f"    No NaN values found ✓")
    
    # Remove duplicates
    print("\n[3] Removing duplicate genes...")
    initial_genes = len(df)
    df = df.drop_duplicates(subset='Gene', keep='first')
    duplicates_removed = initial_genes - len(df)
    print(f"    Duplicates removed: {duplicates_removed}")
    print(f"    After deduplication: {len(df)} genes")
    
    # Save curated data
    print(f"\n[4] Saving curated dataset...")
    df.to_csv(output_file, sep='\t', index=False)
    print(f"    Saved to: {output_file}")
    
    print("\n" + "=" * 70)
    print("✓ PHASE 1 COMPLETE")
    print("=" * 70 + "\n")
    
    return df

if __name__ == "__main__":
    curate_data('data/GSE31210.tsv')
