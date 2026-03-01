# Gene Expression Analysis and Redundancy Removal for Early-Stage Lung Cancer Detection

## Lab Evaluation 1: Data Curation and Feature Engineering

A comprehensive bioinformatics pipeline for preprocessing gene expression data from early-stage lung cancer detection, developed by four undergraduate researchers from Amrita Vishwa Vidyapeetham.

---

## 📋 Table of Contents

- [Team Members](#team-members)
- [Project Overview](#project-overview)
- [Key Statistics](#key-statistics)
- [Pipeline Architecture](#pipeline-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Results](#results)
- [Features Extracted](#features-extracted)
- [License](#license)
- [Contact](#contact)

---

## 👥 Team Members

| Name | Student ID | Role | Email |
|------|-----------|------|-------|
| **Ajeet Gupta** | BL.SC.U4AIE24167 | Data Curation Lead | bl.sc.u4aie24167@bl.students.amrita.edu |
| **B. Deva Harsha** | BL.SC.U4AIE24111 | Redundancy Removal Engineer | bl.sc.u4aie24111@bl.students.amrita.edu |
| **Mamidi Yeswanth** | BL.SC.U4AIE24131 | Clustering Specialist | bl.sc.u4aie24131@bl.students.amrita.edu |
| **K. B. Sohith Chowdary** | BL.SC.U4AIE24124 | Feature Engineer | bl.sc.u4aie24124@bl.students.amrita.edu |

**Department:** Artificial Intelligence  
**Institution:** Amrita Vishwa Vidyapeetham, Bengaluru, India

---

## 🎯 Project Overview

This project demonstrates a systematic, team-based approach to gene expression data preprocessing essential for clinical bioinformatics. Using the Gene Expression Omnibus (GEO) dataset GSE31210, we process 18,000+ genes through four critical phases to identify non-redundant, biologically significant genes suitable for machine learning applications.

### Objectives

- ✅ Reduce computational complexity in machine learning models
- ✅ Improve model interpretability and clinical applicability
- ✅ Minimize false positives and negatives in diagnostic applications
- ✅ Enable cost-effective targeted gene expression assays
- ✅ Create ML-ready feature matrix from raw gene expression data

---

## 📊 Key Statistics

| Metric | Value | Notes |
|--------|-------|-------|
| **Original Genes** | 18,000+ | From GSE31210 dataset |
| **After Curation** | 17,920 | Removed NaN & duplicates |
| **After Redundancy Removal** | 892 | Pearson correlation r > 0.95 |
| **Final Representatives** | 287 | Hierarchical clustering |
| **Dimensionality Reduction** | **98.4%** | Significant compression |
| **Features Extracted** | 6 per gene | Statistical features |
| **Data Retention (Phase 1)** | 99.56% | High-quality output |
| **Processing Time** | < 5 minutes | Efficient pipeline |

---

## 🔄 Pipeline Architecture
                      GSE31210.tsv
                    (18,000+ genes)
                          │
                          ▼
                ┌────────────────────┐
                │  PHASE 1           │
                │  DATA CURATION     │
                │  Ajeet Gupta       │
                └���───────┬───────────┘
                         │
               ✓ Remove NaN values
               ✓ Remove duplicates
               ✓ Validate gene IDs
               ✓ Quality metrics
                         │
                         ▼
             curated_data.tsv
              (17,920 genes)
                         │
                         ▼
                ┌────────────────────┐
                │  PHASE 2           │
                │  REDUNDANCY        │
                │  REMOVAL           │
                │  B. Deva Harsha    │
                └────────┬───────────┘
                         │
               ✓ Compute correlations
               ✓ Identify redundant genes
               ✓ Remove (r > 0.95)
               ✓ Generate statistics
                         │
                         ▼
          non_redundant_data.tsv
              (892 genes, 95% ↓)
                         │
                         ▼
                ┌────────────────────┐
                │  PHASE 3           │
                │  SIMILARITY        │
                │  CLUSTERING        │
                │  Mamidi Yeswanth   │
                └────────┬───────────┘
                         │
               ✓ Hierarchical clustering
               ✓ Correlation distance
               ✓ 60% similarity threshold
               ✓ Cluster representatives
               ✓ Dendrogram visualization
                         │
                         ▼
        selected_similar_genes.tsv
             (287 genes, 287 clusters)
                         │
                         ▼
                ┌────────────────────┐
                │  PHASE 4           │
                │  FEATURE           │
                │  EXTRACTION        │
                │  K. B. Sohith      │
                │  Chowdary          │
                └────────┬───────────┘
                         │
               ✓ Statistical features
               ✓ Feature validation
               ✓ ML-ready matrix
                         │
                         ▼
           extracted_features.tsv
               (287 genes × 6 features)
                    1,722 features
                         │
                         ▼
                  FINAL OUTPUT
                ML-Ready Dataset




---

## 💻 Installation

### System Requirements

- **OS:** macOS, Linux, or Windows
- **Python:** 3.10 or higher
- **RAM:** 4GB minimum
- **Disk Space:** 500MB (with data)

### Prerequisites

'''bash'''
# Check Python version
python --version  # Should be 3.10+

# Check pip
pip --version


git clone https://github.com/ajeetgupta7/Early-Stage-Lung-Cancer-Detection.git
cd Early-Stage-Lung-Cancer-Detection
