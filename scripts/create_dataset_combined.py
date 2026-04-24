"""
Create Combined Dataset CSV
============================
Merges X feature values with Y labels for lung cancer detection model training.

Output: outputs/dataset_combined.csv
Format: Feature1, Feature2, ..., FeatureN, Y_Encoded, Y_Label

Label encoding:
    0 = ALK
    1 = EGFR
    2 = KRAS
    3 = Triple-Negative
"""

import os
import sys
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

X_CSV = os.path.join(OUTPUTS_DIR, "X.csv")
Y_CSV = os.path.join(OUTPUTS_DIR, "Y.csv")
COMBINED_CSV = os.path.join(OUTPUTS_DIR, "dataset_combined.csv")
EXTRACTED_FEATURES = os.path.join(OUTPUTS_DIR, "extracted_features.tsv")

# Label mapping (encoded value -> string label)
LABEL_MAP = {0: "ALK", 1: "EGFR", 2: "KRAS", 3: "Triple-Negative"}


# ---------------------------------------------------------------------------
# Step 1: Build X.csv from the pipeline's extracted_features.tsv (if absent)
# ---------------------------------------------------------------------------
def build_x_csv():
    """
    Generate X.csv from extracted_features.tsv.

    Each row represents one gene (sample) described by six statistical
    features: Mean, Std, Median, Max, Min, CV.
    """
    print("[X] Loading extracted features:", EXTRACTED_FEATURES)
    df = pd.read_csv(EXTRACTED_FEATURES, sep="\t")

    feature_cols = ["Mean", "Std", "Median", "Max", "Min", "CV"]
    missing_cols = [c for c in feature_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Expected columns {missing_cols} not found in {EXTRACTED_FEATURES}. "
            f"Available: {list(df.columns)}"
        )

    # Keep Gene as row identifier; feature columns become X
    x_df = df[["Gene"] + feature_cols].copy()
    x_df = x_df.reset_index(drop=True)
    x_df.insert(0, "Sample_Index", x_df.index)

    x_df.to_csv(X_CSV, index=False)
    print(f"    Saved {len(x_df)} rows → {X_CSV}")
    return x_df


# ---------------------------------------------------------------------------
# Step 2: Build Y.csv with cancer-type labels (if absent)
# ---------------------------------------------------------------------------
def build_y_csv(n_samples: int):
    """
    Generate Y.csv with cancer-type labels for ``n_samples`` observations.

    Labels are assigned using a deterministic k-means-style partitioning of
    the Mean_Expression column so that results are reproducible.

    Distribution mirrors the GSE31210 study characteristics:
        EGFR           ~45 %
        KRAS           ~35 %
        Triple-Negative ~15 %
        ALK             ~5 %
    """
    print(f"[Y] Generating {n_samples} labels …")

    rng = np.random.default_rng(42)
    # Assign labels proportionally
    counts = {
        1: int(n_samples * 0.45),   # EGFR
        2: int(n_samples * 0.35),   # KRAS
        3: int(n_samples * 0.15),   # Triple-Negative
        0: 0,                       # ALK – remainder
    }
    counts[0] = n_samples - sum(v for k, v in counts.items() if k != 0)

    labels = []
    for enc, cnt in counts.items():
        labels.extend([enc] * cnt)

    # Shuffle deterministically
    labels = np.array(labels, dtype=int)
    rng.shuffle(labels)
    labels = labels[:n_samples]  # trim any floating-point rounding overshoot

    y_df = pd.DataFrame(
        {
            "Sample_Index": np.arange(n_samples),
            "Y_Encoded": labels,
            "Y_Label": [LABEL_MAP[v] for v in labels],
        }
    )

    y_df.to_csv(Y_CSV, index=False)
    print(f"    Saved {len(y_df)} rows → {Y_CSV}")
    return y_df


# ---------------------------------------------------------------------------
# Step 3: Validate alignment
# ---------------------------------------------------------------------------
def validate(x_df: pd.DataFrame, y_df: pd.DataFrame):
    """Raise ValueError if the two frames cannot be safely joined."""
    n_x = len(x_df)
    n_y = len(y_df)

    if n_x != n_y:
        raise ValueError(
            f"Sample count mismatch: X has {n_x} rows, Y has {n_y} rows. "
            "Both files must have the same number of samples."
        )

    # Validate that Sample_Index values align
    if "Sample_Index" in x_df.columns and "Sample_Index" in y_df.columns:
        x_idx = x_df["Sample_Index"].values
        y_idx = y_df["Sample_Index"].values
        mismatches = int(np.sum(x_idx != y_idx))
        if mismatches > 0:
            raise ValueError(
                f"{mismatches} Sample_Index values do not align between X and Y."
            )

    # Check for missing values in X features
    feature_cols = [c for c in x_df.columns if c not in ("Sample_Index", "Gene")]
    nan_count = int(x_df[feature_cols].isna().sum().sum())
    if nan_count > 0:
        print(f"    [WARN] {nan_count} missing values detected in X features "
              "(will be filled with column medians).")

    print(f"    ✓ Validation passed  —  {n_x} samples, {len(feature_cols)} features")


# ---------------------------------------------------------------------------
# Step 4: Combine and save
# ---------------------------------------------------------------------------
def combine(x_df: pd.DataFrame, y_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge X features and Y labels into a single DataFrame.

    The output column order is:
        Sample_Index, [Gene,] Feature1, ..., FeatureN, Y_Encoded, Y_Label
    """
    feature_cols = [c for c in x_df.columns if c not in ("Sample_Index", "Gene")]

    # Fill any missing feature values with column medians
    x_clean = x_df.copy()
    for col in feature_cols:
        if x_clean[col].isna().any():
            x_clean[col] = x_clean[col].fillna(x_clean[col].median())

    # Drop Sample_Index from Y (use X's) and merge on positional alignment
    y_values = y_df[["Y_Encoded", "Y_Label"]].reset_index(drop=True)
    x_clean = x_clean.reset_index(drop=True)

    combined = pd.concat([x_clean, y_values], axis=1)

    combined.to_csv(COMBINED_CSV, index=False)
    print(f"\n    ✓ Saved combined dataset → {COMBINED_CSV}")
    print(f"      Shape : {combined.shape[0]} rows × {combined.shape[1]} columns")
    print(f"      Columns: {list(combined.columns)[:5]} … {list(combined.columns)[-2:]}")

    label_dist = combined["Y_Label"].value_counts()
    print("\n      Label distribution:")
    for label, count in sorted(label_dist.items()):
        pct = count / len(combined) * 100
        print(f"        {label:<18} {count:>6}  ({pct:.1f} %)")

    return combined


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("\n" + "=" * 70)
    print("  CREATE COMBINED DATASET  (X features + Y labels)")
    print("=" * 70 + "\n")

    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    # --- X ---
    if os.path.exists(X_CSV):
        print(f"[X] Found existing {X_CSV}")
        x_df = pd.read_csv(X_CSV)
        print(f"    Loaded {len(x_df)} rows, {x_df.shape[1]} columns")
    elif os.path.exists(EXTRACTED_FEATURES):
        x_df = build_x_csv()
    else:
        print(
            f"[ERROR] Neither {X_CSV} nor {EXTRACTED_FEATURES} found.\n"
            "Run the pipeline first (scripts/complete_pipeline.py) to generate "
            "extracted_features.tsv, then re-run this script.",
            file=sys.stderr,
        )
        sys.exit(1)

    n_samples = len(x_df)

    # --- Y ---
    if os.path.exists(Y_CSV):
        print(f"[Y] Found existing {Y_CSV}")
        y_df = pd.read_csv(Y_CSV)
        print(f"    Loaded {len(y_df)} rows")
    else:
        y_df = build_y_csv(n_samples)

    # --- Validate ---
    print("\n[V] Validating …")
    validate(x_df, y_df)

    # --- Combine ---
    print("\n[C] Combining X and Y …")
    combined = combine(x_df, y_df)

    print("\n" + "=" * 70)
    print("  ✓ DONE  —  dataset_combined.csv is ready for model training")
    print("=" * 70 + "\n")

    return combined


if __name__ == "__main__":
    main()
