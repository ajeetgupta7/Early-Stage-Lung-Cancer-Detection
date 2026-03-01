"""
Complete Gene Expression Analysis Pipeline
All 4 phases automated
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from step1_data_curation import curate_data
from step2_redundancy_removal import remove_redundancy
from step3_similarity_clustering import cluster_genes
from step4_feature_extraction import extract_features

def run_complete_pipeline(input_file='data/GSE31210.tsv'):
    """Run complete analysis pipeline"""
    
    print("\n" + "=" * 70)
    print("COMPLETE GENE EXPRESSION ANALYSIS PIPELINE")
    print("=" * 70 + "\n")
    
    os.makedirs('outputs', exist_ok=True)
    
    print("\n>>> EXECUTING PHASE 1: DATA CURATION")
    df1 = curate_data(input_file)
    
    print("\n>>> EXECUTING PHASE 2: REDUNDANCY REMOVAL")
    df2 = remove_redundancy('outputs/curated_data.tsv')
    
    print("\n>>> EXECUTING PHASE 3: SIMILARITY CLUSTERING")
    df3 = cluster_genes('outputs/non_redundant_data.tsv')
    
    print("\n>>> EXECUTING PHASE 4: FEATURE EXTRACTION")
    df4 = extract_features('outputs/selected_similar_genes.tsv')
    
    print("\n" + "=" * 70)
    print("PIPELINE SUMMARY")
    print("=" * 70)
    print(f"\nPhase 1 Output: {df1.shape[0]} genes")
    print(f"Phase 2 Output: {df2.shape[0]} genes")
    print(f"Phase 3 Output: {df3.shape[0]} genes")
    print(f"Phase 4 Output: {df4.shape[0]} genes × {df4.shape[1]-1} features")
    print(f"\nDimensionality Reduction: {100*(1 - df4.shape[0]/18000):.2f}%")
    print("\n✓ PIPELINE EXECUTION COMPLETE")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_complete_pipeline()
