import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Optional
import numpy as np

def create_plots(annotations_df: pd.DataFrame, output_dir: str = 'plots') -> None:
    """
    Creates and saves visualizations for variant annotations.
    
    Args:
        annotations_df (pd.DataFrame): DataFrame containing variant annotations
        output_dir (str): Directory to save the plots
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style for all plots
    plt.style.use('seaborn')
    
    # 1. Bar chart of variants by clinical significance
    plt.figure(figsize=(12, 6))
    
    # Split clinical significance strings and count occurrences
    all_significance = []
    for sig in annotations_df['clinical_significance']:
        if pd.notna(sig) and sig:
            all_significance.extend(sig.split(','))
    
    significance_counts = pd.Series(all_significance).value_counts()
    
    # Plot
    ax = significance_counts.plot(kind='bar', color='skyblue')
    plt.title('Number of Variants by Clinical Significance')
    plt.xlabel('Clinical Significance')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on top of bars
    for i, v in enumerate(significance_counts):
        ax.text(i, v + 0.5, str(v), ha='center')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/clinical_significance.png')
    plt.close()
    
    # 2. Grouped bar chart of allele frequencies
    plt.figure(figsize=(14, 8))
    
    # Select top 10 variants by total frequency for better visualization
    annotations_df['total_freq'] = annotations_df[['SAS_freq', 'AFR_freq', 'EUR_freq']].sum(axis=1)
    top_variants = annotations_df.nlargest(10, 'total_freq')
    
    # Prepare data for plotting
    plot_data = top_variants.melt(
        id_vars=['rsID'],
        value_vars=['SAS_freq', 'AFR_freq', 'EUR_freq'],
        var_name='Population',
        value_name='Frequency'
    )
    
    # Clean up population names
    plot_data['Population'] = plot_data['Population'].str.replace('_freq', '')
    
    # Plot
    ax = sns.barplot(
        data=plot_data,
        x='rsID',
        y='Frequency',
        hue='Population',
        palette='viridis'
    )
    
    plt.title('Allele Frequencies of Top Variants Across Populations')
    plt.xlabel('Variant (rsID)')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Population')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/allele_frequencies.png')
    plt.close()
    
    # 3. Table of top 5 SAS variants
    plt.figure(figsize=(12, 4))
    
    # Get top 5 SAS variants
    top_sas = annotations_df.nlargest(5, 'SAS_freq')[['rsID', 'SAS_freq', 'clinical_significance', 'most_severe_consequence']]
    
    # Create table
    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    
    table = plt.table(
        cellText=top_sas.values,
        colLabels=['rsID', 'SAS Frequency', 'Clinical Significance', 'Consequence'],
        loc='center',
        cellLoc='center'
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    
    plt.title('Top 5 Variants by South Asian (SAS) Frequency')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_sas_variants.png')
    plt.close()

if __name__ == "__main__":
    # Example usage
    from hbb_variants import get_variant_annotations
    
    # Get some test variants
    test_rsids = ['rs334', 'rs33930165', 'rs33950507', 'rs33930165', 'rs33930165']
    annotations_df = get_variant_annotations(test_rsids)
    
    # Create visualizations
    create_plots(annotations_df) 