# 🧬 SickleCellVar – Genetic Variant Explorer

**SickleCellVar** is an interactive Streamlit web app designed to explore and visualize genetic variants—specifically those associated with the **HBB** gene, which plays a central role in sickle cell disease and other blood disorders. The tool highlights population-specific allele frequencies and clinical significance to support genetic research and personalized medicine.

## 📋 Project Description

This application allows users to:
- Fetch and analyze genetic variants from the Ensembl REST API
- Visualize variant distributions across different populations
- Compare allele frequencies between South Asian (SAS), African (AFR), and European (EUR) populations
- View clinical significance and consequences of variants
- Analyze both predefined HBB gene variants and custom rsIDs

## 🖼️ Screenshots

### Main Interface
![Main Interface](screenshots/main_interface.png)

### Clinical Significance Distribution
![Clinical Significance](screenshots/clinical_significance.png)

### Population Frequency Comparison
![Population Frequencies](screenshots/allele_frequencies.png)

### Top SAS Variants
![Top SAS Variants](screenshots/top_sas_variants.png)

## 🚀 Installation and Usage

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/thusharsant/SickleCellVar.git
cd SickleCellVar
