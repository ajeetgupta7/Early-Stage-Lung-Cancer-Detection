# Team Contributions - Lab Evaluation 1

## Project: Gene Expression Analysis and Redundancy Removal

---

## Team Members

| Name | ID | Department | Email |
|------|----|----|-------|
| Ajeet Gupta | BL.SC.U4AIE24167 | AI | ajeetgupta7@bl.students.amrita.edu |
| B. Deva Harsha | BL.SC.U4AIE24111 | AI | bl.sc.u4aie24111@bl.students.amrita.edu |
| Mamidi Yeswanth | BL.SC.U4AIE24131 | AI | bl.sc.u4aie24131@bl.students.amrita.edu |
| K. B. Sohith Chowdary | BL.SC.U4AIE24124 | AI | bl.sc.u4aie24124@bl.students.amrita.edu |

---

## Individual Contributions

### Ajeet Gupta (BL.SC.U4AIE24167) - Data Curation Lead

**Phase:** 1 - Data Curation
**Key Achievement:** 99.56% data retention with high-quality output

- Sourced GSE31210 dataset from NCBI GEO
- Removed NaN values (50 genes)
- Removed duplicates (30 genes)
- Generated curated_data.tsv (17,920 genes)

---

### B. Deva Harsha (BL.SC.U4AIE24111) - Redundancy Removal Engineer

**Phase:** 2 - Redundancy Removal
**Key Achievement:** 95% dimensionality reduction

- Designed Pearson correlation algorithm
- Computed correlation matrix (17,920 × 17,920)
- Identified redundant genes (r > 0.95)
- Generated non_redundant_data.tsv (892 genes)

---

### Mamidi Yeswanth (BL.SC.U4AIE24131) - Clustering Specialist

**Phase:** 3 - Similarity-Based Clustering
**Key Achievement:** Identified 287 co-regulated gene groups

- Implemented hierarchical clustering
- Selected correlation distance metric
- Created dendrogram visualization
- Generated selected_similar_genes.tsv (287 genes)

---

### K. B. Sohith Chowdary (BL.SC.U4AIE24124) - Feature Engineer

**Phase:** 4 - Feature Extraction
**Key Achievement:** ML-ready feature matrix

- Designed feature extraction pipeline
- Computed 6 statistical features per gene
- Performed feature validation
- Generated extracted_features.tsv (287 × 6)

---

**Project Status:** ✓ SUCCESSFULLY COMPLETED
