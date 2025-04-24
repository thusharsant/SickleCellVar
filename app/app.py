import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.append(str(Path(__file__).parent.parent))

from hbb_variants import get_variant_annotations, get_hbb_variants
from visualize_variants import create_plots

# Set page config
st.set_page_config(
    page_title="Genetic Variant Explorer",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS for better formatting
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .stDataFrame {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Title and description
    st.title("🧬 Genetic Variant Explorer")
    st.markdown("""
    This app allows you to explore genetic variants in the HBB gene and other regions of interest.
    You can view variant annotations, population frequencies, and clinical significance.
    """)
    
    # Sidebar for user inputs
    st.sidebar.title("Options")
    
    # Input selection
    input_type = st.sidebar.radio(
        "What would you like to analyze?",
        ["HBB Gene Variants", "Custom rsID"]
    )
    
    # Population selection
    st.sidebar.subheader("Population Comparison")
    show_sas = st.sidebar.checkbox("South Asian (SAS)", value=True)
    show_afr = st.sidebar.checkbox("African (AFR)", value=True)
    show_eur = st.sidebar.checkbox("European (EUR)", value=True)
    
    # Get user input
    if input_type == "Custom rsID":
        rsid_input = st.sidebar.text_input("Enter rsID (e.g., rs334)", "")
        if rsid_input:
            rsids = [rsid.strip() for rsid in rsid_input.split(",")]
        else:
            rsids = []
    else:
        rsids = []
    
    # Process button
    if st.sidebar.button("Generate Analysis"):
        with st.spinner("Processing..."):
            try:
                # Get variant data
                if input_type == "HBB Gene Variants":
                    variants_df = get_hbb_variants()
                    if not variants_df.empty:
                        rsids = variants_df['rsID'].tolist()
                elif rsids:
                    variants_df = pd.DataFrame({'rsID': rsids})
                else:
                    st.warning("Please enter at least one rsID")
                    return
                
                # Get annotations
                annotations_df = get_variant_annotations(rsids)
                
                if annotations_df.empty:
                    st.error("No variant data found. Please check your input.")
                    return
                
                # Filter populations based on selection
                pop_cols = []
                if show_sas:
                    pop_cols.append('SAS_freq')
                if show_afr:
                    pop_cols.append('AFR_freq')
                if show_eur:
                    pop_cols.append('EUR_freq')
                
                if not pop_cols:
                    st.warning("Please select at least one population to compare")
                    return
                
                # Create visualizations
                create_plots(annotations_df)
                
                # Display results
                st.subheader("Variant Annotations")
                st.dataframe(annotations_df)
                
                # Display plots
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Clinical Significance")
                    if os.path.exists("plots/clinical_significance.png"):
                        st.image("plots/clinical_significance.png")
                    else:
                        st.warning("Clinical significance plot not available")
                
                with col2:
                    st.subheader("Population Frequencies")
                    if os.path.exists("plots/allele_frequencies.png"):
                        st.image("plots/allele_frequencies.png")
                    else:
                        st.warning("Population frequencies plot not available")
                
                st.subheader("Top Variants in South Asian Population")
                if os.path.exists("plots/top_sas_variants.png"):
                    st.image("plots/top_sas_variants.png")
                else:
                    st.warning("Top variants table not available")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Display instructions if no analysis has been run
    if not st.session_state.get('analysis_run', False):
        st.info("""
        👈 Use the sidebar to:
        1. Choose between HBB gene variants or custom rsID
        2. Select populations to compare
        3. Click 'Generate Analysis' to view results
        """)

if __name__ == "__main__":
    main() 