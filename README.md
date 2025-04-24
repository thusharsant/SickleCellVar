# 🧬 Genetic Variant Explorer

A Streamlit web application for exploring and visualizing genetic variants, with a focus on the HBB gene and population-specific allele frequencies.

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
git clone https://github.com/yourusername/genetic-variant-explorer.git
cd genetic-variant-explorer
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run app/app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## 💡 Example Use Cases

### Analyzing HBB Gene Variants
1. Select "HBB Gene Variants" in the sidebar
2. Choose populations to compare (SAS, AFR, EUR)
3. Click "Generate Analysis"
4. View the results and visualizations

### Analyzing Custom Variants
1. Select "Custom rsID" in the sidebar
2. Enter one or more rsIDs (comma-separated), e.g., "rs334,rs33930165"
3. Choose populations to compare
4. Click "Generate Analysis"
5. View the results and visualizations

## 📊 Sample Output

When analyzing the HBB gene variants, you might see:
- A table of variant annotations
- A bar chart showing distribution of clinical significance
- A grouped bar chart comparing allele frequencies across populations
- A table of top variants in the South Asian population

## 🛠️ Project Structure

```
genetic-variant-explorer/
├── app/
│   └── app.py              # Streamlit application
├── hbb_variants.py         # Variant data fetching module
├── visualize_variants.py   # Visualization module
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── screenshots/            # Screenshots for documentation
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Data provided by the Ensembl REST API
- Built with Streamlit, pandas, and matplotlib 