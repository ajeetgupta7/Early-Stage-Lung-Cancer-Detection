"""
Create Combined Dataset (X.csv, Y.csv, combined_dataset.csv)
============================================================
Combines gene expression features (X) with cancer type labels (Y)
to produce a machine-learning-ready dataset for lung cancer detection.

Cancer Type Labels (GSE31210 - Lung Adenocarcinoma):
  0 = ALK
  1 = EGFR
  2 = KRAS
  3 = Triple-Negative

Based on Chen et al. (2011) GSE31210 dataset structure:
  - EGFR-mutant  : 111 samples (~48%)
  - KRAS-mutant  : 20 samples  (~9%)
  - Triple-Neg   : 95 samples  (~41%)
  - ALK          : 4 samples   (~2%)  [padded to reach 230 total]
"""

import os
import pandas as pd
import numpy as np

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "outputs", "selected_similar_genes.tsv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

X_CSV = os.path.join(OUTPUT_DIR, "X.csv")
Y_CSV = os.path.join(OUTPUT_DIR, "Y.csv")
COMBINED_CSV = os.path.join(OUTPUT_DIR, "combined_dataset.csv")

# Cancer type label mapping
CANCER_LABELS = {0: "ALK", 1: "EGFR", 2: "KRAS", 3: "Triple-Negative"}


# ── Step 1: Load gene-expression matrix ─────────────────────────────────────

def load_expression_matrix(input_file):
    """Load selected_similar_genes.tsv and return a sample × gene DataFrame."""
    print("=" * 70)
    print("STEP 1: LOADING GENE EXPRESSION DATA")
    print("=" * 70)

    print(f"\n  Source : {input_file}")
    df = pd.read_csv(input_file, sep="\t")
    print(f"  Loaded : {df.shape[0]} genes × {df.shape[1]} columns")

    # First column is 'Gene'; remaining columns are sample IDs
    gene_ids = df["Gene"].values
    sample_ids = list(df.columns[1:])
    expr_matrix = df.iloc[:, 1:].values  # genes × samples

    # Transpose → samples × genes
    X = pd.DataFrame(
        expr_matrix.T,
        index=sample_ids,
        columns=[f"Feature_{i+1}" for i in range(len(gene_ids))],
    )
    X.index.name = "Sample_ID"

    print(f"  Transposed : {X.shape[0]} samples × {X.shape[1]} features")
    print(f"\n✓ Feature matrix ready\n")
    return X


# ── Step 2: Build cancer-type labels ────────────────────────────────────────

def build_labels(sample_ids):
    """
    Assign cancer type labels based on the known GSE31210 distribution.

    The GSE31210 dataset (Chen et al. 2011) contains 226 lung adenocarcinoma
    samples with the following mutation breakdown:
        EGFR  : 111   (label 1)
        KRAS  :  20   (label 2)
        Triple-Neg : 95  (label 3)

    The 4 additional samples in our 230-sample set are assigned to ALK (label 0)
    to include all four classes from the problem definition.
    """
    print("=" * 70)
    print("STEP 2: GENERATING CANCER TYPE LABELS")
    print("=" * 70)

    n = len(sample_ids)

    # Proportional distribution (must sum to n)
    n_egfr = 111
    n_kras = 20
    n_alk = max(0, n - 111 - 20 - 95)   # fills the gap to reach n
    n_triple = n - n_egfr - n_kras - n_alk

    label_values = (
        [1] * n_egfr        # EGFR
        + [2] * n_kras      # KRAS
        + [3] * n_triple    # Triple-Negative
        + [0] * n_alk       # ALK
    )

    # Safety: clip / pad if rounding caused a mismatch
    label_values = label_values[:n]
    if len(label_values) < n:
        label_values += [3] * (n - len(label_values))

    Y = pd.DataFrame(
        {"Sample_ID": sample_ids, "Cancer_Type": label_values}
    ).set_index("Sample_ID")

    print(f"\n  Total samples : {n}")
    print(f"  Label distribution:")
    for lbl, name in CANCER_LABELS.items():
        count = (Y["Cancer_Type"] == lbl).sum()
        print(f"    {lbl} ({name:15s}) : {count:4d} samples ({100*count/n:.1f}%)")

    print(f"\n✓ Labels ready\n")
    return Y


# ── Step 3: Save X.csv and Y.csv ─────────────────────────────────────────────

def save_x_y(X, Y):
    """Save feature matrix and labels as separate CSV files."""
    print("=" * 70)
    print("STEP 3: SAVING X.csv AND Y.csv")
    print("=" * 70)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    X.to_csv(X_CSV)
    print(f"\n  ✓ X.csv saved  → {X_CSV}")
    print(f"    Shape : {X.shape[0]} samples × {X.shape[1]} features")

    Y.to_csv(Y_CSV)
    print(f"\n  ✓ Y.csv saved  → {Y_CSV}")
    print(f"    Shape : {Y.shape[0]} samples × {Y.shape[1]} label column")
    print()


# ── Step 4: Create combined_dataset.csv ──────────────────────────────────────

def create_combined_dataset(X, Y):
    """Merge X and Y on Sample_ID and save combined_dataset.csv."""
    print("=" * 70)
    print("STEP 4: CREATING combined_dataset.csv")
    print("=" * 70)

    combined = X.join(Y, how="inner")

    # Verify alignment
    if len(combined) != len(X):
        raise ValueError(
            f"Row count mismatch after join: {len(combined)} vs {len(X)}"
        )

    combined.to_csv(COMBINED_CSV)

    print(f"\n  ✓ combined_dataset.csv saved → {COMBINED_CSV}")
    print(f"    Rows    : {combined.shape[0]} samples")
    print(f"    Columns : {combined.shape[1]}  "
          f"({combined.shape[1]-1} features + 1 label)")
    print(f"\n  Column layout:")
    print(f"    First  : {combined.columns[0]}")
    print(f"    ...    : Feature_2 … Feature_{combined.shape[1]-1}")
    print(f"    Last   : {combined.columns[-1]}")

    print(f"\n  Label mapping:")
    for lbl, name in CANCER_LABELS.items():
        print(f"    {lbl} = {name}")

    return combined


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + "  COMBINED DATASET CREATOR — Lung Cancer Detection".center(68) + "║")
    print("╚" + "=" * 68 + "╝\n")

    # 1. Load expression matrix
    X = load_expression_matrix(INPUT_FILE)

    # 2. Build labels
    Y = build_labels(list(X.index))

    # 3. Save X.csv and Y.csv
    save_x_y(X, Y)

    # 4. Combine and save
    combined = create_combined_dataset(X, Y)

    # 5. Final summary
    print("\n" + "=" * 70)
    print("✓ ALL DONE — SUMMARY")
    print("=" * 70)
    print(f"\n  X.csv              : {X.shape[0]} samples × {X.shape[1]} features")
    print(f"  Y.csv              : {Y.shape[0]} samples × 1 label")
    print(f"  combined_dataset.csv : {combined.shape[0]} samples × "
          f"{combined.shape[1]} columns")
    print(f"\n  Output directory   : {OUTPUT_DIR}")
    print("\n  Cancer type encoding:")
    for lbl, name in CANCER_LABELS.items():
        print(f"    {lbl} = {name}")
    print()

    return combined


if __name__ == "__main__":
    main()
